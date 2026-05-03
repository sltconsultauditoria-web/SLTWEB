import os
from uuid import uuid4

import pytest


if os.environ.get("RUN_REAL_MONGO_TESTS") != "1":
    pytest.skip("RUN_REAL_MONGO_TESTS=1 nao configurado", allow_module_level=True)


from fastapi.testclient import TestClient
from pymongo import MongoClient

from backend.main_enterprise import app, db
from backend.workers.async_jobs import create_job


client = TestClient(app)


def _payload(response):
    body = response.json()
    if isinstance(body, dict) and isinstance(body.get("data"), dict):
        return body["data"]
    return body


def test_real_mongo_crud_and_persistence_roundtrip():
    marker = f"real-persistence-{uuid4()}"
    created_ids = {name: [] for name in ["empresas", "documentos", "alertas", "pipeline_events", "jobs"]}

    try:
        empresa_response = client.post(
            "/api/empresas",
            json={
                "nome": "Empresa Teste Persistencia",
                "cnpj": "00999999000191",
                "test_marker": marker,
            },
        )
        assert empresa_response.status_code == 200
        empresa = _payload(empresa_response)
        empresa_id = empresa.get("id")
        assert empresa_id
        created_ids["empresas"].append(empresa_id)

        empresas_response = client.get("/api/empresas")
        assert empresas_response.status_code == 200
        assert marker in empresas_response.text

        documento_response = client.post(
            "/api/documentos",
            json={
                "empresa_id": empresa_id,
                "nome": "Documento Teste Persistencia",
                "tipo": "teste",
                "test_marker": marker,
            },
        )
        assert documento_response.status_code == 200
        documento = _payload(documento_response)
        assert documento.get("id")
        created_ids["documentos"].append(documento["id"])

        alerta_response = client.post(
            "/api/alertas",
            json={
                "empresa_id": empresa_id,
                "titulo": "Alerta Teste Persistencia",
                "descricao": "Alerta criado por teste real",
                "prioridade": "alta",
                "test_marker": marker,
            },
        )
        assert alerta_response.status_code == 200
        alerta = _payload(alerta_response)
        assert alerta.get("id")
        created_ids["alertas"].append(alerta["id"])

        evento_response = client.post(
            "/api/events",
            json={
                "origem": "teste",
                "tipo": "persistencia",
                "empresa_id": empresa_id,
                "severidade": "alta",
                "status": "novo",
                "titulo": "Evento Teste Persistencia",
                "descricao": "Evento criado por teste real",
                "referencia": marker,
                "test_marker": marker,
            },
        )
        assert evento_response.status_code == 200
        evento = _payload(evento_response)
        assert evento.get("id")
        created_ids["pipeline_events"].append(evento["id"])

        job = create_job("persistence_probe", {"test_marker": marker}, max_attempts=1)
        assert job.get("id")
        created_ids["jobs"].append(job["id"])

        fresh_client = MongoClient(os.environ.get("MONGO_URL") or os.environ.get("MONGO_URI"))
        fresh_db = fresh_client[os.environ.get("DB_NAME") or "consultslt_db"]
        assert fresh_db["empresas"].find_one({"test_marker": marker})
        assert fresh_db["documentos"].find_one({"test_marker": marker})
        assert fresh_db["alertas"].find_one({"test_marker": marker})
        assert fresh_db["pipeline_events"].find_one({"referencia": marker})
        assert fresh_db["jobs"].find_one({"payload.test_marker": marker})
    finally:
        for collection_name in created_ids:
            db[collection_name].delete_many({"test_marker": marker})
        db["pipeline_events"].delete_many({"referencia": marker})
        db["jobs"].delete_many({"payload.test_marker": marker})
        db["alertas"].delete_many({"referencia": marker})
