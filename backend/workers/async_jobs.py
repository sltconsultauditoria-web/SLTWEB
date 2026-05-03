from __future__ import annotations

import os
import threading
from datetime import datetime
from time import perf_counter
from typing import Any, Callable

try:
    import redis  # type: ignore
    from rq import Queue  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    redis = None
    Queue = None

from bson import ObjectId


JOB_COLLECTION = "jobs"
JOB_LOG_COLLECTION = "job_logs"
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


def record_job_log(
    *,
    job_id: str,
    provider: str,
    status: str,
    duration_ms: int,
    mode: str | None = None,
    error: str | None = None,
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    document = {
        "job_id": job_id,
        "provider": provider,
        "status": status,
        "duration_ms": duration_ms,
        "mode": mode,
        "error": error,
        "details": details or {},
        "created_at": now(),
    }
    result = job_db()[JOB_LOG_COLLECTION].insert_one(document)
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


def job_metrics() -> dict[str, Any]:
    logs = list(job_db()[JOB_LOG_COLLECTION].find({}))
    jobs_ok = sum(1 for item in logs if str(item.get("status")) == "done")
    jobs_error = sum(1 for item in logs if str(item.get("status")) == "error")
    duration_values = [int(item.get("duration_ms") or 0) for item in logs if int(item.get("duration_ms") or 0) > 0]
    avg_duration = round(sum(duration_values) / len(duration_values), 2) if duration_values else 0
    last_success = None
    for item in sorted(logs, key=lambda row: row.get("created_at") or ""):
        if str(item.get("status")) == "done":
            last_success = item.get("created_at")
    return {
        "jobs_ok": jobs_ok,
        "jobs_error": jobs_error,
        "avg_duration": avg_duration,
        "last_success_at": last_success,
        "providers": sorted({str(item.get("provider") or "") for item in logs if item.get("provider")}),
        "total_logs": len(logs),
    }


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
    start = perf_counter()
    existing_document = None
    document_id = str(payload.get("id") or payload.get("ocr_id") or payload.get("documento_id") or "").strip() or None
    if document_id:
        existing_document = app_module.db["ocr_documentos"].find_one(app_module.object_query(document_id))
    if not existing_document and isinstance(payload.get("documento"), dict):
        existing_document = payload["documento"]

    processed = app_module.process_ocr_payload(payload, existing_document)
    stored = app_module.persist_ocr_document(processed, existing_id=document_id)
    app_module.log_ocr_processing(document_id, payload, stored)
    record_job_log(
        job_id=str(job.get("id") or ""),
        provider="ocr",
        status="done",
        duration_ms=int((perf_counter() - start) * 1000),
        mode="simulado",
        details={"documento_id": stored.get("id"), "status": stored.get("status")},
    )
    return {"ocr_documento": stored}


def _process_fiscal_pipeline_job(job: dict[str, Any]) -> dict[str, Any]:
    import backend.main_enterprise as app_module

    start = perf_counter()
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
        provider_start = perf_counter()
        ecac_contract = app_module.ecac_service.consultar_status(cnpj)
        ecac_duration = int((perf_counter() - provider_start) * 1000)
        provider_start = perf_counter()
        pgdas_contract = app_module.pgdas_service.consultar_pgdas(cnpj)
        pgdas_duration = int((perf_counter() - provider_start) * 1000)
        provider_start = perf_counter()
        sefaz_contract = app_module.sefaz_service.consultar_nfe(cnpj)
        sefaz_duration = int((perf_counter() - provider_start) * 1000)
        government_checks.append(
            {
                "empresa_id": serialized_company.get("id"),
                "cnpj": cnpj,
                "ecac": ecac_contract,
                "pgdas": pgdas_contract,
                "sefaz": sefaz_contract,
            }
        )

        app_module.log_ocr_process_event(
            {
                "job_type": "government_integration",
                "empresa_id": serialized_company.get("id"),
                "created_at": now(),
                "detalhes": {
                    "ecac": ecac_contract,
                    "pgdas": pgdas_contract,
                    "sefaz": sefaz_contract,
                },
            }
        )

        record_job_log(
            job_id=str(job.get("id") or ""),
            provider="ecac",
            status="done" if ecac_contract.get("success") else "error",
            duration_ms=ecac_duration,
            mode=str(ecac_contract.get("mode") or "simulado"),
            error=(ecac_contract.get("errors") or [None])[0],
            details={"empresa_id": serialized_company.get("id")},
        )
        record_job_log(
            job_id=str(job.get("id") or ""),
            provider="pgdas",
            status="done" if pgdas_contract.get("success") else "error",
            duration_ms=pgdas_duration,
            mode=str(pgdas_contract.get("mode") or "simulado"),
            error=(pgdas_contract.get("errors") or [None])[0],
            details={"empresa_id": serialized_company.get("id")},
        )
        record_job_log(
            job_id=str(job.get("id") or ""),
            provider="sefaz",
            status="done" if sefaz_contract.get("success") else "error",
            duration_ms=sefaz_duration,
            mode=str(sefaz_contract.get("mode") or "simulado"),
            error=(sefaz_contract.get("errors") or [None])[0],
            details={"empresa_id": serialized_company.get("id")},
        )

    record_job_log(
        job_id=str(job.get("id") or ""),
        provider="fiscal_pipeline",
        status="done",
        duration_ms=int((perf_counter() - start) * 1000),
        mode="simulado",
        details={"eventos": len(pipeline_result.get("events", [])), "decisions_created": decisions_created},
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
    start = perf_counter()
    ecac_contract = app_module.ecac_service.consultar_status(cnpj)
    pgdas_contract = app_module.pgdas_service.consultar_pgdas(cnpj, payload.get("periodo"))
    sefaz_contract = app_module.sefaz_service.consultar_nfe(cnpj, payload.get("periodo"))
    duration_ms = int((perf_counter() - start) * 1000)
    record_job_log(
        job_id=str(job.get("id") or ""),
        provider="government_integration",
        status="done",
        duration_ms=duration_ms,
        mode=mode,
        details={
            "cnpj": cnpj,
            "ecac": ecac_contract,
            "pgdas": pgdas_contract,
            "sefaz": sefaz_contract,
        },
    )
    return {
        "mode": mode,
        "ecac": ecac_contract,
        "pgdas": pgdas_contract,
        "sefaz": sefaz_contract,
    }


def _process_email_notification_job(job: dict[str, Any]) -> dict[str, Any]:
    from backend.services.email_service import send_email_notification

    raw_payload = job.get("payload") or {}
    notification = raw_payload.get("notification") if isinstance(raw_payload.get("notification"), dict) else raw_payload
    start = perf_counter()
    result = send_email_notification(notification)
    status = "done" if result.get("sent") or result.get("mode") in {"log_only", "skipped"} else "error"
    log_document = {
        "job_id": str(job.get("id") or ""),
        "status": status,
        "mode": result.get("mode"),
        "reason": result.get("reason"),
        "subject": notification.get("subject"),
        "destinatarios": result.get("recipients") or notification.get("destinatarios") or [],
        "tipo": notification.get("tipo"),
        "prioridade": notification.get("prioridade") or notification.get("severidade"),
        "notification": notification,
        "created_at": now(),
        "duration_ms": int((perf_counter() - start) * 1000),
    }
    inserted = job_db()["email_logs"].insert_one(log_document)
    log_document["_id"] = inserted.inserted_id
    log_document["id"] = str(inserted.inserted_id)
    record_job_log(
        job_id=str(job.get("id") or ""),
        provider="email",
        status=status,
        duration_ms=log_document["duration_ms"],
        mode=str(result.get("mode") or "smtp"),
        error=result.get("reason") if status == "error" else None,
        details={"recipients": len(log_document["destinatarios"]), "tipo": log_document["tipo"]},
    )
    return {"email": result, "log_id": log_document["id"]}


def _process_notification_dispatch_job(job: dict[str, Any]) -> dict[str, Any]:
    from backend.services.notification_service import dispatch_notification

    raw_payload = job.get("payload") or {}
    notification = raw_payload.get("notification") if isinstance(raw_payload.get("notification"), dict) else raw_payload
    start = perf_counter()
    result = dispatch_notification(job_db(), str(job.get("id") or ""), notification)
    status = "error" if result.get("errors") else "done"
    record_job_log(
        job_id=str(job.get("id") or ""),
        provider="notification_dispatch",
        status=status,
        duration_ms=int((perf_counter() - start) * 1000),
        mode="async",
        error="notification_delivery_failed" if result.get("errors") else None,
        details={"channels": [item.get("channel") for item in result.get("channels", [])]},
    )
    return result


def process_job(job_id: str) -> dict[str, Any]:
    job = load_job(job_id)
    if not job:
        raise ValueError("Job nao encontrado")

    job = serialize_job(job)
    attempts = max(1, int(job.get("attempts") or 0))
    update_job(job_id, {"status": "processing", "attempts": attempts, "started_at": now(), "error": None})
    started = perf_counter()

    try:
        job_type = str(job.get("job_type") or "").lower()
        if job_type == "ocr_process":
            result = _process_ocr_job(job)
        elif job_type == "fiscal_pipeline":
            result = _process_fiscal_pipeline_job(job)
        elif job_type == "government_integration":
            result = _process_government_job(job)
        elif job_type == "email_notification":
            result = _process_email_notification_job(job)
        elif job_type == "notification_dispatch":
            result = _process_notification_dispatch_job(job)
        else:
            result = {"message": "Job executado sem handler especifico", "payload": job.get("payload")}

        max_attempts = int(job.get("max_attempts") or 3)
        if job_type == "notification_dispatch" and result.get("retrying") and attempts < max_attempts:
            retry_at = None
            retry_logs = [
                item.get("next_retry_at")
                for item in result.get("retrying", [])
                if item.get("next_retry_at")
            ]
            if retry_logs:
                retry_at = retry_logs[0]
            updated = update_job(
                job_id,
                {
                    "status": "pending",
                    "attempts": attempts + 1,
                    "result": result,
                    "error": None,
                    "next_retry_at": retry_at or now(),
                    "duration_ms": int((perf_counter() - started) * 1000),
                },
            )
            enqueue_job(job_id)
            return updated

        finished = update_job(
            job_id,
            {
                "status": "done",
                "result": result,
                "error": None,
                "finished_at": now(),
                "duration_ms": int((perf_counter() - started) * 1000),
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
                "duration_ms": int((perf_counter() - started) * 1000),
            },
        )
        record_job_log(
            job_id=job_id,
            provider=str(job.get("job_type") or "job"),
            status="error",
            duration_ms=int((perf_counter() - started) * 1000),
            mode="simulado",
            error=str(exc),
        )
        return failure
