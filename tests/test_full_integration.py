from pathlib import Path

import pytest
from fastapi.testclient import TestClient

import backend.main_enterprise as app_module
from tests.test_api_endpoints import FakeClient, make_db


@pytest.fixture()
def client(monkeypatch):
    monkeypatch.setattr(app_module, "db", make_db())
    monkeypatch.setattr(app_module, "client", FakeClient())
    return TestClient(app_module.app)


def test_full_integration_backend_smoke_and_persistence(client):
    health = client.get("/health", follow_redirects=False)
    assert health.status_code == 200
    assert health.json()["data"]["mongo"] in {"ok", "erro"}

    login = client.post("/api/auth/login", json={"email": "admin@consultslt.com", "password": "senha"})
    assert login.status_code == 200
    token = login.json()["data"]["token"]
    assert token

    headers = {"Authorization": f"Bearer {token}"}

    dashboard = client.get("/api/dashboard", headers=headers)
    assert dashboard.status_code == 200
    assert dashboard.json()["data"]["alertas"] >= 0

    alertas = client.get("/api/alertas", headers=headers)
    assert alertas.status_code == 200
    assert isinstance(alertas.json()["data"], list)

    config = client.get("/api/alerts/config", headers=headers)
    assert config.status_code == 200
    assert config.json()["data"]["email_enabled"] is True

    smtp = client.post(
        "/api/alerts/config/smtp",
        headers=headers,
        json={"host": "smtp.local", "port": 587, "username": "user", "password": "secret", "from_email": "alertas@local"},
    )
    assert smtp.status_code == 200
    assert smtp.json()["data"]["success"] is True
    assert app_module.db["alerts_config"].find_one({"id": "default"})["smtp"]["host"] == "smtp.local"

    recipient = client.post(
        "/api/alerts/recipients",
        headers=headers,
        json={"name": "Financeiro", "email": "financeiro@empresa.com", "whatsapp": "+5511999999999"},
    )
    assert recipient.status_code == 200
    recipient_id = recipient.json()["data"]["id"]
    assert app_module.db["alerts_recipients"].find_one({"id": recipient_id})["email"] == "financeiro@empresa.com"

    updated = client.put(
        f"/api/alerts/recipients/{recipient_id}",
        headers=headers,
        json={"name": "Financeiro 2", "email": "financeiro2@empresa.com", "whatsapp": "+5511888888888"},
    )
    assert updated.status_code == 200
    assert app_module.db["alerts_recipients"].find_one({"id": recipient_id})["name"] == "Financeiro 2"

    deleted = client.delete(f"/api/alerts/recipients/{recipient_id}", headers=headers)
    assert deleted.status_code == 200
    assert app_module.db["alerts_recipients"].find_one({"id": recipient_id}) is None

    preview = client.get("/api/alerts/preview", headers=headers)
    assert preview.status_code == 200
    assert isinstance(preview.json()["data"], list)

    check = client.post("/api/alerts/check-and-notify", headers=headers)
    assert check.status_code == 200
    assert "notified" in check.json()["data"]

    timeline = client.get("/api/empresas/1/timeline", headers=headers)
    assert timeline.status_code in {200, 404}

    jobs = client.get("/api/jobs", headers=headers)
    assert jobs.status_code == 200
    assert isinstance(jobs.json()["data"], list)


def test_frontend_does_not_contain_known_bad_url_patterns():
    src_root = Path("frontend/src")
    patterns = ["/api/api", "/undefined/api"]
    collected = "\n".join(path.read_text(encoding="utf-8", errors="ignore") for path in src_root.rglob("*") if path.is_file())
    for pattern in patterns:
        assert pattern not in collected


def test_legacy_static_files_removed():
    assert not Path("frontend/src/pages/DashboardEnterprise.jsx").exists()
    assert not Path("frontend/src/pages/FiscalList.jsx").exists()
    assert not Path("frontend/src/pages/__read_Obrigacoes.txt").exists()
