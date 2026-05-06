import pytest
from fastapi.testclient import TestClient

import backend.main_enterprise as app_module
from backend.seeds.seed_obrigacoes_acessorias import seed_obrigacoes_acessorias
from tests.test_api_endpoints import FakeClient, make_db


@pytest.fixture()
def app_db(monkeypatch):
    fake_db = make_db()
    monkeypatch.setattr(app_module, "db", fake_db)
    monkeypatch.setattr(app_module, "client", FakeClient())
    seed_obrigacoes_acessorias(app_module.db, force=True)
    return fake_db


@pytest.fixture()
def client(app_db):
    return TestClient(app_module.app)


@pytest.fixture()
def admin_headers():
    return auth_headers("admin", "admin@empresa.com")


@pytest.fixture()
def viewer_headers():
    return auth_headers("viewer", "viewer1@empresa.com")


def auth_headers(role="admin", email=None):
    email = email or f"{role}@empresa.com"
    token = app_module.create_access_token(
        {
            "sub": email,
            "email": email,
            "role": role,
            "perfil": role,
            "name": role.title(),
        }
    )
    return {"Authorization": f"Bearer {token}"}

