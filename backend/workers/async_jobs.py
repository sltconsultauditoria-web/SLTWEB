from __future__ import annotations

import os
import threading
from datetime import datetime
from typing import Any, Callable

try:
    import redis  # type: ignore
    from rq import Queue  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    redis = None
    Queue = None

from bson import ObjectId


JOB_COLLECTION = "jobs"
LOCAL_JOB_LOCK = threading.Lock()
LOCAL_JOB_QUEUE: list[str] = []
LOCAL_WORKER_STARTED = False


def now() -> str:
    return datetime.utcnow().isoformat()


def job_db():
    import backend.main_enterprise as app_module

    return app_module.db


def serialize_job(document: dict[str, Any]) -> dict[str, Any]:
    from backend.main_enterprise import serialize

    serialized = serialize(document)
    serialized["id"] = str(serialized.get("id") or serialized.get("_id"))
    return serialized


def job_query(job_id: str) -> dict[str, Any]:
    if ObjectId.is_valid(job_id):
        return {"_id": ObjectId(job_id)}
    return {"id": job_id}


def load_job(job_id: str) -> dict[str, Any] | None:
    return job_db()[JOB_COLLECTION].find_one(job_query(job_id))


def persist_job(document: dict[str, Any]) -> dict[str, Any]:
    result = job_db()[JOB_COLLECTION].insert_one(document)
    document["_id"] = result.inserted_id
    document["id"] = str(result.inserted_id)
    return serialize_job(document)


def update_job(job_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    payload = {**payload, "updated_at": now()}
    job_db()[JOB_COLLECTION].update_one(job_query(job_id), {"$set": payload}, upsert=False)
    stored = load_job(job_id)
    return serialize_job(stored or {"id": job_id, **payload})


def create_job(job_type: str, payload: dict[str, Any], *, max_attempts: int = 3) -> dict[str, Any]:
    document = {
        "job_type": job_type,
        "status": "pending",
        "attempts": 0,
        "max_attempts": max_attempts,
        "payload": payload,
        "result": None,
        "error": None,
        "created_at": now(),
        "updated_at": now(),
    }
    stored = persist_job(document)
    enqueue_job(stored["id"])
    return stored


def list_jobs(limit: int = 100, status: str | None = None, job_type: str | None = None) -> list[dict[str, Any]]:
    query: dict[str, Any] = {}
    if status:
        query["status"] = status
    if job_type:
        query["job_type"] = job_type
    items = list(job_db()[JOB_COLLECTION].find(query).sort("created_at", -1).limit(limit))
    return [serialize_job(item) for item in items]


def retry_job(job_id: str) -> dict[str, Any]:
    stored = load_job(job_id)
    if not stored:
        raise ValueError("Job nao encontrado")
    if str(stored.get("status")) == "processing":
        raise ValueError("Job em processamento")
    attempts = int(stored.get("attempts") or 0) + 1
    updated = update_job(
        job_id,
        {
            "status": "pending",
            "attempts": attempts,
            "error": None,
            "updated_at": now(),
            "retried_at": now(),
        },
    )
    enqueue_job(job_id)
    return updated


def _use_redis_queue() -> bool:
    enabled = str(os.environ.get("ASYNC_USE_REDIS", "1")).strip().lower() in {"1", "true", "yes", "on"}
    return bool(enabled and redis and Queue and os.environ.get("REDIS_URL"))


def _rq_enqueue(job_id: str) -> None:
    if not _use_redis_queue():
        return
    from redis import Redis  # type: ignore

    connection = Redis.from_url(os.environ["REDIS_URL"])
    queue = Queue("consultslt-jobs", connection=connection)
    queue.enqueue(process_job, job_id, job_timeout=1800)


def _ensure_local_worker() -> None:
    global LOCAL_WORKER_STARTED
    if LOCAL_WORKER_STARTED:
        return

    def _worker_loop() -> None:
        while True:
            job_id = None
            with LOCAL_JOB_LOCK:
                if LOCAL_JOB_QUEUE:
                    job_id = LOCAL_JOB_QUEUE.pop(0)
            if not job_id:
                threading.Event().wait(0.1)
                continue
            process_job(job_id)

    thread = threading.Thread(target=_worker_loop, daemon=True, name="consultslt-local-worker")
    thread.start()
    LOCAL_WORKER_STARTED = True


def enqueue_job(job_id: str) -> None:
    if _use_redis_queue():
        _rq_enqueue(job_id)
        return

    _ensure_local_worker()
    with LOCAL_JOB_LOCK:
        LOCAL_JOB_QUEUE.append(job_id)


def _process_ocr_job(job: dict[str, Any]) -> dict[str, Any]:
    import backend.main_enterprise as app_module

    raw_payload = job.get("payload") or {}
    payload = raw_payload.get("payload") if isinstance(raw_payload.get("payload"), dict) else raw_payload
    existing_document = None
    document_id = str(payload.get("id") or payload.get("ocr_id") or payload.get("documento_id") or "").strip() or None
    if document_id:
        existing_document = app_module.db["ocr_documentos"].find_one(app_module.object_query(document_id))
    if not existing_document and isinstance(payload.get("documento"), dict):
        existing_document = payload["documento"]

    processed = app_module.process_ocr_payload(payload, existing_document)
    stored = app_module.persist_ocr_document(processed, existing_id=document_id)
    app_module.log_ocr_processing(document_id, payload, stored)
    return {"ocr_documento": stored}


def _process_fiscal_pipeline_job(job: dict[str, Any]) -> dict[str, Any]:
    import backend.main_enterprise as app_module

    pipeline_result = app_module.run_fiscal_pipeline_once()
    summary = pipeline_result.get("summary") or {}
    decisions_created = 0
    for event in pipeline_result.get("events", []):
        if str(event.get("severidade") or "").lower() not in {"alta", "critica"}:
            continue
        decision = app_module.decision_engine.analyze(event)
        decision["pipeline_event_id"] = event.get("id")
        decision["created_from"] = "fiscal_pipeline"
        app_module.db["decision_actions"].insert_one(decision)
        decisions_created += 1

    companies = list(app_module.db["empresas"].find({}))
    government_checks: list[dict[str, Any]] = []
    for company in companies:
        serialized_company = app_module.serialize(company)
        cnpj = serialized_company.get("cnpj")
        if not cnpj:
            continue
        ecac_status = app_module.ecac_service.status(cnpj)
        pgdas_status = app_module.pgdas_service.consultar(cnpj)
        sefaz_status = app_module.sefaz_service.consultar_nfe(cnpj)
        government_checks.append(
            {
                "empresa_id": serialized_company.get("id"),
                "cnpj": cnpj,
                "ecac": ecac_status,
                "pgdas": pgdas_status,
                "sefaz": sefaz_status,
            }
        )

        app_module.log_ocr_process_event(
            {
                "job_type": "government_integration",
                "empresa_id": serialized_company.get("id"),
                "created_at": now(),
                "detalhes": {
                    "ecac": ecac_status,
                    "pgdas": pgdas_status,
                    "sefaz": sefaz_status,
                },
            }
        )

    return {
        "summary": summary,
        "decisions_created": decisions_created,
        "government_checks": len(government_checks),
        "checks": government_checks[:10],
    }


def _process_government_job(job: dict[str, Any]) -> dict[str, Any]:
    import backend.main_enterprise as app_module

    raw_payload = job.get("payload") or {}
    payload = raw_payload.get("payload") if isinstance(raw_payload.get("payload"), dict) else raw_payload
    cnpj = payload.get("cnpj")
    if not cnpj:
        raise ValueError("CNPJ obrigatorio")
    mode = str(payload.get("mode") or "simulated").lower()
    return {
        "mode": mode,
        "ecac": app_module.ecac_service.status(cnpj),
        "pgdas": app_module.pgdas_service.consultar(cnpj, payload.get("periodo")),
        "sefaz": app_module.sefaz_service.consultar_nfe(cnpj, payload.get("periodo")),
    }


def process_job(job_id: str) -> dict[str, Any]:
    job = load_job(job_id)
    if not job:
        raise ValueError("Job nao encontrado")

    job = serialize_job(job)
    attempts = max(1, int(job.get("attempts") or 0))
    update_job(job_id, {"status": "processing", "attempts": attempts, "started_at": now(), "error": None})

    try:
        job_type = str(job.get("job_type") or "").lower()
        if job_type == "ocr_process":
            result = _process_ocr_job(job)
        elif job_type == "fiscal_pipeline":
            result = _process_fiscal_pipeline_job(job)
        elif job_type == "government_integration":
            result = _process_government_job(job)
        else:
            result = {"message": "Job executado sem handler especifico", "payload": job.get("payload")}

        finished = update_job(
            job_id,
            {
                "status": "done",
                "result": result,
                "error": None,
                "finished_at": now(),
            },
        )
        return finished
    except Exception as exc:
        failure = update_job(
            job_id,
            {
                "status": "error",
                "error": str(exc),
                "finished_at": now(),
            },
        )
        return failure
