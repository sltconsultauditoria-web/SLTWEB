from datetime import datetime
from pathlib import Path
import tempfile

from bson import ObjectId

import backend.main_enterprise as app_module


def test_cors_preflight_allows_github_pages_origin(client):
    origin = "https://sltconsultauditoria-web.github.io"
    response = client.options(
        "/api/obrigacoes/dashboard",
        headers={
            "Origin": origin,
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "authorization,content-type",
        },
        follow_redirects=False,
    )

    assert response.status_code < 400, response.text
    assert response.headers.get("access-control-allow-origin") in {origin, "*"}
    assert "access-control-allow-methods" in response.headers

    allowed_methods = response.headers["access-control-allow-methods"]
    for method in ["GET", "POST", "PUT", "DELETE", "OPTIONS"]:
        assert method in allowed_methods


def test_serialize_handles_objectid_datetime_and_null_fields():
    payload = {
        "_id": ObjectId(),
        "created_at": datetime(2026, 5, 6, 12, 30),
        "content_type": None,
        "nested": {"updated_at": datetime(2026, 5, 6, 12, 31), "value": None},
    }

    serialized = app_module.serialize(payload)

    assert isinstance(serialized["id"], str)
    assert serialized["created_at"].startswith("2026-05-06T12:30:00")
    assert serialized["content_type"] is None
    assert serialized["nested"]["value"] is None
    assert serialized["nested"]["updated_at"].startswith("2026-05-06T12:31:00")


def test_objectid_and_datetime_documents_do_not_generate_500(client, app_db, admin_headers):
    item_id = str(ObjectId())
    app_module.db["auditorias"].insert_one(
        {
            "_id": ObjectId(item_id),
            "id": item_id,
            "created_at": datetime(2026, 5, 6, 12, 0),
            "score_conformidade": 100,
            "campo_null": None,
        }
    )

    response = client.get(f"/api/auditoria/{item_id}", headers=admin_headers, follow_redirects=False)
    assert response.status_code == 200, response.text
    assert response.status_code != 500
    assert isinstance(response.json()["data"]["id"], str)


def test_absent_document_content_type_uses_default_without_500(client, app_db, admin_headers):
    base_tmp = Path(tempfile.gettempdir()) / "sltweb-tests"
    base_tmp.mkdir(parents=True, exist_ok=True)
    arquivo = base_tmp / "sem-tipo.dat"
    arquivo.write_bytes(b"arquivo sem tipo")
    item_id = str(ObjectId())
    app_module.db["documentos"].insert_one(
        {
            "_id": ObjectId(item_id),
            "id": item_id,
            "nome_arquivo": "sem-tipo.dat",
            "caminho_arquivo": str(arquivo),
        }
    )

    response = client.get(f"/api/documentos/{item_id}/download", headers=admin_headers, follow_redirects=False)

    assert response.status_code == 200, response.text
    assert response.status_code != 500
    assert response.headers["content-type"].startswith("application/octet-stream")

