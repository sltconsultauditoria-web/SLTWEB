from copy import deepcopy

import pytest
from bson import ObjectId
from fastapi.testclient import TestClient

import backend.main_enterprise as app_module


class FakeInsertResult:
    def __init__(self, inserted_id):
        self.inserted_id = inserted_id


class FakeUpdateResult:
    def __init__(self, matched_count=0, modified_count=0, upserted_id=None):
        self.matched_count = matched_count
        self.modified_count = modified_count
        self.upserted_id = upserted_id


class FakeDeleteResult:
    def __init__(self, deleted_count):
        self.deleted_count = deleted_count


class FakeCursor:
    def __init__(self, items):
        self._items = [deepcopy(item) for item in items]

    def sort(self, key, direction=1):
        self._items.sort(key=lambda item: item.get(key), reverse=direction == -1)
        return self

    def limit(self, count):
        self._items = self._items[:count]
        return self

    def to_list(self, length=None):
        if length is None:
            return [deepcopy(item) for item in self._items]
        return [deepcopy(item) for item in self._items[:length]]

    def __iter__(self):
        return iter([deepcopy(item) for item in self._items])


def _matches(document, query):
    if not query:
        return True

    for key, expected in query.items():
        if key == "$and":
            return all(_matches(document, subquery) for subquery in expected)

        value = document.get(key)
        if isinstance(expected, dict):
            for operator, operand in expected.items():
                if operator == "$in" and value not in operand:
                    return False
                if operator == "$nin" and value in operand:
                    return False
                if operator == "$ne" and value == operand:
                    return False
                if operator == "$exists":
                    exists = key in document and document.get(key) is not None
                    if bool(operand) != exists:
                        return False
                if operator == "$gte" and value < operand:
                    return False
                if operator == "$lte" and value > operand:
                    return False
                if operator == "$gt" and value <= operand:
                    return False
                if operator == "$lt" and value >= operand:
                    return False
        else:
            if str(value) != str(expected):
                return False
    return True


class FakeCollection:
    def __init__(self, items=None):
        self.items = [deepcopy(item) for item in (items or [])]

    def find(self, query=None, projection=None):
        return FakeCursor([item for item in self.items if _matches(item, query or {})])

    def find_one(self, query=None, projection=None):
        for item in self.items:
            if _matches(item, query or {}):
                return deepcopy(item)
        return None

    def count_documents(self, query=None):
        return sum(1 for item in self.items if _matches(item, query or {}))

    def insert_one(self, document):
        stored = deepcopy(document)
        stored.setdefault("_id", ObjectId())
        self.items.append(stored)
        return FakeInsertResult(stored["_id"])

    def update_one(self, query, update, upsert=False):
        for index, item in enumerate(self.items):
            if _matches(item, query or {}):
                if "$set" in update:
                    self.items[index] = {**item, **deepcopy(update["$set"])}
                else:
                    self.items[index] = {**item, **deepcopy(update)}
                return FakeUpdateResult(matched_count=1, modified_count=1)

        if upsert:
            stored = deepcopy(query or {})
            payload = deepcopy(update.get("$set", update))
            stored.update(payload)
            stored.setdefault("_id", ObjectId())
            self.items.append(stored)
            return FakeUpdateResult(matched_count=0, modified_count=1, upserted_id=stored["_id"])

        return FakeUpdateResult()

    def delete_one(self, query):
        for index, item in enumerate(self.items):
            if _matches(item, query or {}):
                self.items.pop(index)
                return FakeDeleteResult(1)
        return FakeDeleteResult(0)


class FakeAdmin:
    def command(self, _command):
        return {"ok": 1}


class FakeClient:
    admin = FakeAdmin()


class FakeDB:
    def __init__(self, collections):
        self._collections = collections
        self.name = "consultslt_db"

    def __getitem__(self, item):
        if item not in self._collections:
            self._collections[item] = FakeCollection([])
        return self._collections[item]


def make_db():
    return FakeDB(
        {
        "empresas": FakeCollection(
            [
                {"_id": ObjectId(), "nome": "Empresa A", "ativo": True, "status": "ativa"},
                {"_id": ObjectId(), "nome": "Empresa B", "ativo": False, "status": "inativa"},
            ]
        ),
        "documentos": FakeCollection(
            [
                {"_id": ObjectId(), "nome": "Documento 1", "status": "processado", "created_at": "2026-05-01T10:00:00"},
            ]
        ),
        "guias": FakeCollection([{"_id": ObjectId(), "status": "concluida"}]),
        "obrigacoes": FakeCollection(
            [
                {"_id": ObjectId(), "status": "pendente", "vencimento": "2026-05-10"},
                {"_id": ObjectId(), "status": "entregue", "vencimento": "2026-05-01"},
            ]
        ),
        "alertas": FakeCollection(
            [
                {"_id": ObjectId(), "titulo": "Critico 1", "prioridade": "critica", "status": "pendente", "lido": False, "resolvido": False, "created_at": "2026-05-01T09:00:00"},
                {"_id": ObjectId(), "titulo": "Critico 2", "prioridade": "alta", "status": "aberto", "lido": False, "resolvido": False, "created_at": "2026-05-01T10:00:00"},
                {"_id": ObjectId(), "titulo": "Resolvido", "prioridade": "media", "status": "resolvido", "lido": True, "resolvido": True, "created_at": "2026-05-01T11:00:00"},
            ]
        ),
        "auditorias": FakeCollection([{"_id": ObjectId(), "score": 95, "created_at": "2026-05-01T12:00:00"}]),
        "ocr_documentos": FakeCollection(
            [
                {"_id": ObjectId(), "status": "processado"},
                {"_id": ObjectId(), "status": "pendente"},
                {"_id": ObjectId(), "status": "erro", "nome_arquivo": "arquivo-erro.pdf"},
            ]
        ),
        "robots": FakeCollection([{"_id": ObjectId(), "status": "idle"}]),
        "robot_files": FakeCollection([{"_id": ObjectId(), "nome": "file-a.pdf"}]),
        "robot_history": FakeCollection([{"_id": ObjectId(), "acao": "run"}]),
        "sharepoint": FakeCollection([]),
        "tipos_relatorios": FakeCollection([{"_id": ObjectId(), "nome": "Fiscal"}]),
        "relatorios": FakeCollection([{"_id": ObjectId(), "nome": "Relatorio 1"}]),
        "certidoes": FakeCollection([{"_id": ObjectId(), "cnpj": "12345678000100", "tipo": "CND", "data_validade": "2026-05-04", "status": "vigente"}]),
        "debitos": FakeCollection([{"_id": ObjectId(), "cnpj": "12345678000100", "status": "aberto"}]),
        "pipeline_events": FakeCollection([]),
        "fiscal_pipeline_logs": FakeCollection([]),
        "usuarios": FakeCollection([]),
        "fiscal_data": FakeCollection([]),
        }
    )


@pytest.fixture()
def client(monkeypatch):
    monkeypatch.setattr(app_module, "db", make_db())
    monkeypatch.setattr(app_module, "client", FakeClient())
    return TestClient(app_module.app)


@pytest.mark.parametrize(
    "method,path,kwargs",
    [
        ("GET", "/health", {}),
        ("GET", "/api/dashboard", {}),
        ("POST", "/api/auth/login", {"json": {"email": "admin@consultslt.com", "password": "senha"}}),
        ("GET", "/api/empresas", {}),
        ("GET", "/api/documentos", {}),
        ("GET", "/api/guias", {}),
        ("GET", "/api/obrigacoes", {}),
        ("GET", "/api/alertas", {}),
        ("GET", "/api/auditoria", {}),
        ("GET", "/api/auditoria/estatisticas", {}),
        ("GET", "/api/ocr/documentos", {}),
        ("GET", "/api/ocr/estatisticas", {}),
        ("GET", "/api/ocr/tipos-suportados", {}),
        ("GET", "/api/robots/ingestion/status", {}),
        ("GET", "/api/robots/ingestion/history", {"params": {"limit": 10}}),
        ("GET", "/api/robots/ingestion/files", {"params": {"limit": 20}}),
        ("GET", "/api/sharepoint/status", {}),
        ("GET", "/api/relatorios", {}),
        ("GET", "/api/tipos_relatorios", {}),
        ("GET", "/api/certidoes", {"params": {"cnpj": "12345678000100"}}),
        ("GET", "/api/debitos", {"params": {"cnpj": "12345678000100"}}),
    ],
)
def test_api_endpoints_return_200(client, method, path, kwargs):
    response = client.request(method, path, follow_redirects=False, **kwargs)
    assert response.status_code == 200, response.text


def test_alertas_are_normalized(client):
    response = client.get("/api/alertas", follow_redirects=False)
    assert response.status_code == 200
    payload = response.json()["data"]
    assert isinstance(payload, list)
    first = payload[0]
    for field in ("id", "titulo", "descricao", "prioridade", "status", "lido", "resolvido", "data"):
        assert field in first


def test_delete_documento_existing_returns_ok(client):
    existing_id = str(app_module.db["documentos"].items[0]["_id"])
    response = client.delete(f"/api/documentos/{existing_id}", follow_redirects=False)
    assert response.status_code in (200, 204)
    assert response.status_code != 404


def test_delete_documento_missing_returns_404(client):
    response = client.delete("/api/documentos/507f1f77bcf86cd799439011", follow_redirects=False)
    assert response.status_code == 404


def test_calcular_das_returns_200(client):
    response = client.post(
        "/api/fiscal/calcular/das",
        json={
            "cnpj": "12345678000100",
            "periodo": "2026-05",
            "receita_bruta_12m": 1200000,
            "receita_mensal": 100000,
            "anexo": "anexo_iii",
        },
        follow_redirects=False,
    )
    assert response.status_code == 200
    payload = response.json()["data"]
    assert payload["status"] == "SUCESSO"
    assert "valor_das" in payload


def test_calcular_fator_r_returns_200(client):
    response = client.post(
        "/api/fiscal/calcular/fator-r",
        json={
            "cnpj": "12345678000100",
            "periodo": "2026-05",
            "folha_salarios_12m": 400000,
            "receita_bruta_12m": 1200000,
        },
        follow_redirects=False,
    )
    assert response.status_code == 200
    payload = response.json()["data"]
    assert payload["status"] == "SUCESSO"
    assert "fator_r_percentual" in payload


def test_events_endpoint_lists_and_creates(client):
    response = client.get("/api/events", follow_redirects=False)
    assert response.status_code == 200
    payload = response.json()["data"]
    assert isinstance(payload, list)

    create_response = client.post(
        "/api/events",
        json={
            "origem": "usuario",
            "tipo": "alerta",
            "empresa_id": "empresa-1",
            "severidade": "critica",
            "titulo": "Evento manual",
            "descricao": "Evento gerado via API",
            "payload": {"origem": "usuario"},
            "referencia": "manual-001",
        },
        follow_redirects=False,
    )
    assert create_response.status_code == 200
    created = create_response.json()["data"]
    assert created["origem"] == "usuario"
    assert created["severidade"] == "critica"
    assert created["titulo"] == "Evento manual"
    assert "alerta" in create_response.json()["data"]


def test_pipeline_run_generates_events_alerts_and_logs(client):
    before_events = app_module.db["pipeline_events"].count_documents({})
    before_alerts = app_module.db["alertas"].count_documents({})

    response = client.post("/api/fiscal/pipeline/run", follow_redirects=False)
    assert response.status_code == 200
    summary = response.json()["data"]
    assert summary["status"] == "sucesso"
    assert summary["eventos_gerados"] >= 3
    assert summary["alertas_gerados"] >= 2

    after_events = app_module.db["pipeline_events"].count_documents({})
    after_alerts = app_module.db["alertas"].count_documents({})
    assert after_events >= before_events + 3
    assert after_alerts >= before_alerts + 2

    status_response = client.get("/api/fiscal/pipeline/status", follow_redirects=False)
    assert status_response.status_code == 200
    status_payload = status_response.json()["data"]
    assert status_payload["last_status"] == "sucesso"
    assert status_payload["eventos_total"] >= after_events

    logs_response = client.get("/api/fiscal/pipeline/logs", follow_redirects=False)
    assert logs_response.status_code == 200
    logs_payload = logs_response.json()["data"]
    assert isinstance(logs_payload, list)
    assert len(logs_payload) >= 2


def test_resolver_evento_marks_resolved(client):
    created = client.post(
        "/api/events",
        json={
            "origem": "fiscal",
            "tipo": "vencimento",
            "empresa_id": "empresa-2",
            "severidade": "alta",
            "titulo": "Vencimento pendente",
            "descricao": "Alerta de vencimento",
            "payload": {"origem": "fiscal"},
            "referencia": "resolver-001",
        },
        follow_redirects=False,
    ).json()["data"]

    resolve_response = client.patch(f"/api/events/{created['id']}/resolver", follow_redirects=False)
    assert resolve_response.status_code == 200
    resolved = resolve_response.json()["data"]
    assert resolved["status"] == "resolvido"

    stored_event = app_module.db["pipeline_events"].find_one({"dedupe_key": created["dedupe_key"]})
    assert stored_event["status"] == "resolvido"
