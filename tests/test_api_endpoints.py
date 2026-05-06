from copy import deepcopy
import time

import pytest
from bson import ObjectId
from fastapi.testclient import TestClient

import backend.main_enterprise as app_module
from backend.integrations.government.ecac_service import GovernmentECACService
from backend.integrations.government.pgdas_service import PGDAService
from backend.integrations.government.sefaz_service import SEFAZService


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

    def delete_many(self, query):
        kept = []
        deleted = 0
        for item in self.items:
            if _matches(item, query or {}):
                deleted += 1
                continue
            kept.append(item)
        self.items = kept
        return FakeDeleteResult(deleted)


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
                {"_id": ObjectId(), "nome": "Empresa A", "razao_social": "Empresa A LTDA", "nome_fantasia": "Empresa A", "cnpj": "12345678000100", "ativo": True, "status": "ativa"},
                {"_id": ObjectId(), "nome": "Empresa B", "razao_social": "Empresa B LTDA", "nome_fantasia": "Empresa B", "cnpj": "99887766000199", "ativo": False, "status": "inativa"},
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
        "ocr_process_logs": FakeCollection([]),
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
        "job_logs": FakeCollection([]),
        "email_logs": FakeCollection([]),
        "notification_channels": FakeCollection([]),
        "notification_preferences": FakeCollection([]),
        "notification_logs": FakeCollection([]),
        "alerts_config": FakeCollection([{"id": "default", "email_enabled": True, "whatsapp_enabled": False, "teams_enabled": False}]),
        "alerts_recipients": FakeCollection([]),
        "alerts_thresholds": FakeCollection([]),
        "alerts_history": FakeCollection([]),
        "decision_actions": FakeCollection([]),
        "subscription_plans": FakeCollection([]),
        "tenants": FakeCollection([]),
        "roles_permissions": FakeCollection([]),
        "jobs": FakeCollection([]),
        "usuarios": FakeCollection([]),
        "fiscal_data": FakeCollection([]),
        }
    )


@pytest.fixture()
def client(monkeypatch):
    monkeypatch.setattr(app_module, "db", make_db())
    monkeypatch.setattr(app_module, "client", FakeClient())
    return TestClient(app_module.app)


def wait_for_job(client, job_id, timeout=5.0):
    deadline = time.time() + timeout
    last_payload = None
    while time.time() < deadline:
        response = client.get(f"/api/jobs/{job_id}", follow_redirects=False)
        assert response.status_code == 200
        last_payload = response.json()["data"]
        if str(last_payload.get("status")) in {"done", "error"}:
            return last_payload
        time.sleep(0.1)
    return last_payload


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


@pytest.mark.parametrize(
    "method,path,kwargs",
    [
        ("GET", "/health", {}),
        ("GET", "/api/dashboard", {}),
        ("POST", "/api/auth/login", {"json": {"email": "admin@empresa.com", "password": "admin123"}}),
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
        ("GET", "/api/relatorios", {"headers": auth_headers("viewer", "viewer1@empresa.com")}),
        ("GET", "/api/tipos_relatorios", {"headers": auth_headers("viewer", "viewer1@empresa.com")}),
        ("GET", "/api/certidoes", {"params": {"cnpj": "12345678000100"}}),
        ("GET", "/api/debitos", {"params": {"cnpj": "12345678000100"}}),
        ("GET", "/api/dashboard/analytics", {}),
        ("GET", "/api/integracoes/ecac/status", {"params": {"cnpj": "12345678000100"}}),
        ("GET", "/api/integracoes/ecac/debitos", {"params": {"cnpj": "12345678000100"}}),
        ("GET", "/api/integracoes/pgdas/consultar", {"params": {"cnpj": "12345678000100"}}),
        ("GET", "/api/integracoes/sefaz/nfe", {"params": {"cnpj": "12345678000100"}}),
        ("GET", "/api/jobs", {}),
        ("GET", "/api/jobs/metrics", {}),
        ("GET", "/api/notificacoes/channels", {}),
        ("GET", "/api/notificacoes/preferences", {}),
        ("GET", "/api/notificacoes/logs", {}),
        ("GET", "/api/notificacoes/metrics", {}),
        ("GET", "/api/notificacoes/email/config", {}),
        ("GET", "/api/notificacoes/email/logs", {}),
        ("GET", "/api/subscriptions/plans", {}),
        ("GET", "/api/tenants", {}),
        ("GET", "/api/rbac/roles-permissions", {}),
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


def test_sharepoint_sync_endpoint_returns_200_without_config(client, monkeypatch):
    monkeypatch.delenv("SHAREPOINT_SITE_URL", raising=False)
    monkeypatch.delenv("SHAREPOINT_DRIVE_ID", raising=False)
    monkeypatch.delenv("SHAREPOINT_SITE_ID", raising=False)
    response = client.post("/api/sharepoint/sync", follow_redirects=False)
    assert response.status_code == 200
    payload = response.json()["data"]
    assert payload["status"] == "log_only"
    assert payload["configured"] is False


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
    job = response.json()["data"]
    assert job["job_type"] == "fiscal_pipeline"
    assert job["status"] in {"pending", "processing", "done"}

    completed = wait_for_job(client, job["id"], timeout=10)
    assert completed["status"] == "done"
    summary = completed["result"]["summary"]
    assert summary["status"] == "sucesso"
    assert summary["eventos_gerados"] >= 3
    assert summary["alertas_gerados"] >= 2
    assert completed["result"]["decisions_created"] >= 1

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


def test_empresa_timeline_returns_events_and_alerts(client):
    empresa_id = str(app_module.db["empresas"].items[0]["_id"])
    app_module.db["documentos"].insert_one(
        {
            "nome": "Documento Timeline",
            "status": "processado",
            "empresa_id": empresa_id,
            "created_at": "2026-05-02T10:00:00",
        }
    )
    app_module.db["obrigacoes"].insert_one(
        {
            "titulo": "Obrigacao Timeline",
            "status": "pendente",
            "empresa_id": empresa_id,
            "vencimento": "2026-05-10",
            "created_at": "2026-05-02T11:00:00",
        }
    )
    client.post(
        "/api/events",
        json={
            "origem": "usuario",
            "tipo": "alerta",
            "empresa_id": empresa_id,
            "severidade": "alta",
            "titulo": "Evento Timeline",
            "descricao": "Evento para timeline",
            "payload": {"empresa_id": empresa_id},
            "referencia": "timeline-001",
        },
        follow_redirects=False,
    )

    response = client.get(f"/api/empresas/{empresa_id}/timeline", follow_redirects=False)
    assert response.status_code == 200
    payload = response.json()["data"]
    assert payload["empresa"]["cnpj"] == "12345678000100"
    assert payload["total"] >= 3
    fontes = {item["fonte"] for item in payload["timeline"]}
    assert "pipeline_events" in fontes
    assert "documentos" in fontes
    assert "obrigacoes" in fontes


def test_timeline_filters_by_status_and_period(client):
    empresa_id = str(app_module.db["empresas"].items[0]["_id"])
    response = client.get(
        f"/api/empresas/{empresa_id}/timeline",
        params={"status": "resolvido", "inicio": "2099-01-01", "fim": "2099-12-31"},
        follow_redirects=False,
    )
    assert response.status_code == 200
    payload = response.json()["data"]
    assert payload["timeline"] == []


def test_export_relatorios_pdf_and_excel(client):
    empresa_id = str(app_module.db["empresas"].items[0]["_id"])

    pdf_response = client.get(
        "/api/relatorios/export/pdf",
        params={"empresa_id": empresa_id},
        headers=auth_headers("viewer", "viewer1@empresa.com"),
        follow_redirects=False,
    )
    assert pdf_response.status_code == 200
    assert "application/pdf" in pdf_response.headers["content-type"]
    assert 'attachment; filename="' in pdf_response.headers["content-disposition"]
    assert pdf_response.content.startswith(b"%PDF")

    excel_response = client.get(
        "/api/relatorios/export/excel",
        params={"empresa_id": empresa_id},
        headers=auth_headers("viewer", "viewer1@empresa.com"),
        follow_redirects=False,
    )
    assert excel_response.status_code == 200
    assert "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" in excel_response.headers["content-type"]
    assert 'attachment; filename="' in excel_response.headers["content-disposition"]
    assert excel_response.content[:2] == b"PK"


def test_relatorios_endpoints_require_bearer_and_allow_viewer_admin(client):
    protected_paths = [
        "/api/relatorios",
        "/api/tipos_relatorios",
        "/api/relatorios/export/pdf",
        "/api/relatorios/export/excel",
    ]
    for path in protected_paths:
        missing = client.get(path, follow_redirects=False)
        assert missing.status_code == 401

        invalid = client.get(path, headers={"Authorization": "Bearer invalid-token"}, follow_redirects=False)
        assert invalid.status_code == 401

        viewer = client.get(path, headers=auth_headers("viewer", "viewer1@empresa.com"), follow_redirects=False)
        assert viewer.status_code == 200

        admin = client.get(path, headers=auth_headers("admin", "admin@empresa.com"), follow_redirects=False)
        assert admin.status_code == 200


def test_relatorios_openapi_and_cors_download_headers(client):
    openapi = client.get("/openapi.json", follow_redirects=False).json()
    assert openapi["paths"]["/api/relatorios"]["get"]["security"] == [{"HTTPBearer": []}]
    assert openapi["paths"]["/api/tipos_relatorios"]["get"]["security"] == [{"HTTPBearer": []}]
    assert openapi["paths"]["/api/relatorios/export/pdf"]["get"]["security"] == [{"HTTPBearer": []}]
    assert openapi["paths"]["/api/relatorios/export/excel"]["get"]["security"] == [{"HTTPBearer": []}]

    response = client.options(
        "/api/relatorios/export/pdf",
        headers={
            "Origin": "https://sltconsultauditoria-web.github.io",
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "authorization,content-type",
        },
        follow_redirects=False,
    )
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "https://sltconsultauditoria-web.github.io"

    download = client.get(
        "/api/relatorios/export/pdf",
        headers={
            **auth_headers("viewer", "viewer1@empresa.com"),
            "Origin": "https://sltconsultauditoria-web.github.io",
        },
        follow_redirects=False,
    )
    assert download.status_code == 200
    assert "Content-Disposition" in download.headers["access-control-expose-headers"]


def test_ocr_process_and_ai_analyze(client):
    response = client.post(
        "/api/ocr/process",
        json={
            "nome_arquivo": "nf_12345678000100_2026-05-10.pdf",
            "texto": "CNPJ 12.345.678/0001-00 Valor R$ 1.234,56 Vencimento 10/05/2026 Nota Fiscal",
            "empresa_id": str(app_module.db["empresas"].items[0]["_id"]),
        },
        follow_redirects=False,
    )
    assert response.status_code == 200
    payload = response.json()["data"]
    assert payload["job_type"] == "ocr_process"
    assert payload["status"] in {"pending", "processing", "done"}

    job = wait_for_job(client, payload["id"])
    assert job["status"] == "done"
    result = job["result"]["ocr_documento"]
    assert result["status"] == "done"
    assert result["dados_extraidos"]["cnpj"] == "12345678000100"
    assert result["dados_extraidos"]["valor"] == 1234.56
    assert str(result["dados_extraidos"]["vencimento"]).startswith("2026-05-10")
    assert app_module.db["ocr_process_logs"].count_documents({}) >= 1

    ai_response = client.post(
        "/api/ocr/ai-analyze",
        json={"texto": "CNPJ 12.345.678/0001-00 Valor R$ 1.234,56 Vencimento 10/05/2026 Nota Fiscal"},
        follow_redirects=False,
    )
    assert ai_response.status_code == 200
    ai_payload = ai_response.json()["data"]
    assert ai_payload["classificacao"] in {"nfe", "nfse", "pgdas", "certidao", "boleto", "guia", "documento"}


def test_integrations_and_decisions_flow(client):
    ecac_status = client.get("/api/integracoes/ecac/status", params={"cnpj": "12345678000100"}, follow_redirects=False)
    assert ecac_status.status_code == 200
    assert ecac_status.json()["data"]["cnpj"] == "12345678000100"
    assert ecac_status.json()["data"]["modo"] == "simulado"

    ecac_debitos = client.get("/api/integracoes/ecac/debitos", params={"cnpj": "12345678000100"}, follow_redirects=False)
    assert ecac_debitos.status_code == 200
    assert isinstance(ecac_debitos.json()["data"]["debitos"], list)

    pgdas = client.get("/api/integracoes/pgdas/consultar", params={"cnpj": "12345678000100"}, follow_redirects=False)
    assert pgdas.status_code == 200
    assert pgdas.json()["data"]["cnpj"] == "12345678000100"
    assert pgdas.json()["data"]["modo"] == "simulado"

    sefaz = client.get("/api/integracoes/sefaz/nfe", params={"cnpj": "12345678000100"}, follow_redirects=False)
    assert sefaz.status_code == 200
    assert isinstance(sefaz.json()["data"]["documentos"], list)
    assert sefaz.json()["data"]["modo"] == "simulado"

    event_response = client.post(
        "/api/events",
        json={
            "origem": "fiscal",
            "tipo": "vencimento",
            "empresa_id": "12345678000100",
            "severidade": "critica",
            "titulo": "Certidao vencendo",
            "descricao": "Evento para motor de decisao",
            "payload": {"empresa_id": "12345678000100"},
            "referencia": "decision-001",
        },
        follow_redirects=False,
    )
    event = event_response.json()["data"]

    decision_response = client.post("/api/decisions", json={"event": event}, follow_redirects=False)
    assert decision_response.status_code == 200
    decision = decision_response.json()["data"]
    assert decision["acao_sugerida"] == "regularizar"

    execute_response = client.post(f"/api/decisions/{decision['id']}/execute", follow_redirects=False)
    assert execute_response.status_code == 200
    executed = execute_response.json()["data"]
    assert executed["status"] == "executado"

    jobs_response = client.get("/api/jobs", follow_redirects=False)
    assert jobs_response.status_code == 200
    jobs_payload = jobs_response.json()["data"]
    assert isinstance(jobs_payload, list)


def test_dashboard_analytics_has_risk_and_trends(client):
    response = client.get("/api/dashboard/analytics", follow_redirects=False)
    assert response.status_code == 200
    payload = response.json()["data"]
    assert "tendencia_mensal" in payload
    assert "ranking_risco" in payload
    assert "saude_fiscal" in payload


def test_job_retry_and_status_flow(client):
    created = client.post(
        "/api/ocr/process",
        json={"nome_arquivo": "arquivo.pdf", "texto": "CNPJ 12.345.678/0001-00"},
        follow_redirects=False,
    ).json()["data"]
    job = wait_for_job(client, created["id"])
    assert job["status"] == "done"
    retry = client.post(f"/api/jobs/{created['id']}/retry", follow_redirects=False)
    assert retry.status_code == 200
    retried = wait_for_job(client, created["id"])
    assert retried["status"] == "done"


def test_monetization_and_rbac_endpoints(client):
    plans = client.get("/api/subscriptions/plans", follow_redirects=False)
    assert plans.status_code == 200
    assert len(plans.json()["data"]) >= 3

    tenants = client.get("/api/tenants", follow_redirects=False)
    assert tenants.status_code == 200
    assert len(tenants.json()["data"]) >= 1

    roles = client.get("/api/rbac/roles-permissions", follow_redirects=False)
    assert roles.status_code == 200
    assert len(roles.json()["data"]) >= 3


def test_me_requires_jwt_and_returns_role(client):
    missing = client.get("/api/me", follow_redirects=False)
    assert missing.status_code == 401

    response = client.get("/api/me", headers=auth_headers("admin", "admin@empresa.com"), follow_redirects=False)
    assert response.status_code == 200
    payload = response.json()["data"]
    assert payload["email"] == "admin@empresa.com"
    assert payload["role"] == "admin"
    assert payload["perfil"] == "admin"


def test_admin_can_create_and_delete_usuario(client):
    created = client.post(
        "/api/usuarios",
        json={"email": "novo.viewer@empresa.com", "nome": "Novo Viewer", "senha": "Viewer@2026", "role": "viewer"},
        headers=auth_headers("admin", "admin@empresa.com"),
        follow_redirects=False,
    )
    assert created.status_code == 201, created.text
    payload = created.json()["data"]
    assert payload["email"] == "novo.viewer@empresa.com"
    assert payload["role"] == "viewer"
    assert payload["perfil"] == "viewer"
    assert "senha" not in payload
    assert "password" not in payload
    assert "senha_hash" not in payload
    assert "senha_hash" in app_module.db["usuarios"].find_one({"email": "novo.viewer@empresa.com"})

    deleted = client.delete(
        f"/api/usuarios/{payload['id']}",
        headers=auth_headers("admin", "admin@empresa.com"),
        follow_redirects=False,
    )
    assert deleted.status_code == 200


def test_viewer_cannot_manage_usuarios(client):
    existing_id = str(ObjectId())
    app_module.db["usuarios"].insert_one(
        {
            "_id": ObjectId(existing_id),
            "email": "target@empresa.com",
            "nome": "Target",
            "role": "viewer",
            "perfil": "viewer",
            "senha_hash": "hash",
        }
    )

    create_response = client.post(
        "/api/usuarios",
        json={"email": "blocked@empresa.com", "nome": "Blocked", "senha": "Viewer@2026"},
        headers=auth_headers("viewer", "viewer1@empresa.com"),
        follow_redirects=False,
    )
    assert create_response.status_code == 403

    delete_response = client.delete(
        f"/api/usuarios/{existing_id}",
        headers=auth_headers("viewer", "viewer1@empresa.com"),
        follow_redirects=False,
    )
    assert delete_response.status_code == 403


def test_usuario_create_requires_token_and_valid_payload(client):
    no_token = client.post(
        "/api/usuarios",
        json={"email": "sem.token@empresa.com", "nome": "Sem Token", "senha": "Viewer@2026"},
        follow_redirects=False,
    )
    assert no_token.status_code == 401

    invalid_payload = client.post(
        "/api/usuarios",
        json={"nome": "Payload Invalido", "senha": "Viewer@2026"},
        headers=auth_headers("admin", "admin@empresa.com"),
        follow_redirects=False,
    )
    assert invalid_payload.status_code == 422


def test_admin_can_manage_viewer_specific_endpoints(client):
    created = client.post(
        "/api/usuarios/viewers",
        json={"email": "viewer.crud@empresa.com", "nome": "Viewer CRUD", "senha": "Viewer@2026", "role": "admin"},
        headers=auth_headers("admin", "admin@empresa.com"),
        follow_redirects=False,
    )
    assert created.status_code == 201, created.text
    payload = created.json()["data"]
    assert payload["role"] == "viewer"
    assert payload["perfil"] == "viewer"
    assert payload["email"] == "viewer.crud@empresa.com"
    stored = app_module.db["usuarios"].find_one({"email": "viewer.crud@empresa.com"})
    assert stored["role"] == "viewer"
    assert "senha_hash" in stored
    assert stored.get("senha") is None

    listed = client.get("/api/usuarios/viewers", headers=auth_headers("admin", "admin@empresa.com"), follow_redirects=False)
    assert listed.status_code == 200
    assert all((item.get("role") or item.get("perfil")) == "viewer" for item in listed.json()["data"])

    updated = client.put(
        f"/api/usuarios/viewers/{payload['id']}",
        json={"nome": "Viewer Editado", "role": "admin"},
        headers=auth_headers("admin", "admin@empresa.com"),
        follow_redirects=False,
    )
    assert updated.status_code == 200
    assert updated.json()["data"]["nome"] == "Viewer Editado"
    assert updated.json()["data"]["role"] == "viewer"

    deleted = client.delete(
        f"/api/usuarios/viewers/{payload['id']}",
        headers=auth_headers("admin", "admin@empresa.com"),
        follow_redirects=False,
    )
    assert deleted.status_code == 200


def test_viewer_and_missing_token_cannot_manage_viewer_endpoints(client):
    no_token = client.post(
        "/api/usuarios/viewers",
        json={"email": "no.token.viewer@empresa.com", "nome": "No Token", "senha": "Viewer@2026"},
        follow_redirects=False,
    )
    assert no_token.status_code == 401

    viewer_create = client.post(
        "/api/usuarios/viewers",
        json={"email": "blocked.viewer@empresa.com", "nome": "Blocked", "senha": "Viewer@2026"},
        headers=auth_headers("viewer", "viewer1@empresa.com"),
        follow_redirects=False,
    )
    assert viewer_create.status_code == 403

    viewer_id = str(ObjectId())
    app_module.db["usuarios"].insert_one(
        {
            "_id": ObjectId(viewer_id),
            "email": "delete.blocked@empresa.com",
            "nome": "Delete Blocked",
            "role": "viewer",
            "perfil": "viewer",
            "senha_hash": "hash",
        }
    )
    viewer_delete = client.delete(
        f"/api/usuarios/viewers/{viewer_id}",
        headers=auth_headers("viewer", "viewer1@empresa.com"),
        follow_redirects=False,
    )
    assert viewer_delete.status_code == 403


def test_last_admin_cannot_be_deleted_or_downgraded(client):
    admin_id = str(ObjectId())
    app_module.db["usuarios"].insert_one(
        {
            "_id": ObjectId(admin_id),
            "email": "only.admin@empresa.com",
            "nome": "Only Admin",
            "role": "admin",
            "perfil": "admin",
            "senha_hash": "hash",
        }
    )

    downgrade = client.put(
        f"/api/usuarios/{admin_id}",
        json={"role": "viewer"},
        headers=auth_headers("admin", "only.admin@empresa.com"),
        follow_redirects=False,
    )
    assert downgrade.status_code == 409

    delete = client.delete(
        f"/api/usuarios/{admin_id}",
        headers=auth_headers("admin", "only.admin@empresa.com"),
        follow_redirects=False,
    )
    assert delete.status_code == 409


def test_viewer_endpoints_are_bearer_protected_in_openapi(client):
    openapi = client.get("/openapi.json", follow_redirects=False).json()
    assert openapi["paths"]["/api/usuarios/viewers"]["get"]["security"] == [{"HTTPBearer": []}]
    assert openapi["paths"]["/api/usuarios/viewers"]["post"]["security"] == [{"HTTPBearer": []}]
    assert openapi["paths"]["/api/usuarios/viewers/{item_id}"]["put"]["security"] == [{"HTTPBearer": []}]
    assert openapi["paths"]["/api/usuarios/viewers/{item_id}"]["delete"]["security"] == [{"HTTPBearer": []}]


def test_government_connectors_simulated_mode(monkeypatch):
    monkeypatch.delenv("ECAC_CLIENT_ID", raising=False)
    monkeypatch.delenv("ECAC_CLIENT_SECRET", raising=False)
    monkeypatch.delenv("ECAC_BASE_URL", raising=False)
    service = GovernmentECACService()
    contract = service.consultar_status("12345678000100")
    assert contract["success"] is True
    assert contract["mode"] == "simulado"
    assert contract["provider"] == "ecac"
    assert contract["data"]["cnpj"] == "12345678000100"

    debt_contract = service.consultar_debitos("12345678000100")
    cert_contract = service.consultar_certidoes("12345678000100")
    assert debt_contract["success"] is True
    assert cert_contract["success"] is True
    assert debt_contract["mode"] == "simulado"
    assert cert_contract["mode"] == "simulado"
    assert debt_contract["provider"] == "ecac"
    assert cert_contract["provider"] == "ecac"


def test_government_connectors_real_mode_with_fallback(monkeypatch):
    monkeypatch.setenv("PGDAS_USERNAME", "user")
    monkeypatch.setenv("PGDAS_PASSWORD", "pass")
    monkeypatch.setenv("PGDAS_BASE_URL", "https://pgdas.example")
    service = PGDAService()
    monkeypatch.setattr(service, "_real_pgdas", lambda cnpj, periodo=None: {"cnpj": cnpj, "periodo_referencia": periodo or "2026-05", "status": "em_dia"})
    contract = service.consultar_pgdas("12345678000100", "2026-05")
    assert contract["success"] is True
    assert contract["mode"] == "real"
    assert contract["provider"] == "pgdas"
    assert contract["data"]["status"] == "em_dia"

    monkeypatch.setenv("SEFAZ_API_URL", "https://sefaz.example")
    monkeypatch.setenv("SEFAZ_API_KEY", "token")
    sefaz = SEFAZService()
    monkeypatch.setattr(sefaz, "_real_nfe", lambda cnpj, periodo=None: (_ for _ in ()).throw(RuntimeError("boom")))
    fallback = sefaz.consultar_nfe("12345678000100")
    assert fallback["success"] is True
    assert fallback["mode"] == "simulado"
    assert fallback["provider"] == "sefaz"
    assert fallback["errors"]


def test_job_metrics_endpoint_reports_processing_stats(client):
    created = client.post(
        "/api/ocr/process",
        json={"nome_arquivo": "job-metrics.pdf", "texto": "CNPJ 12.345.678/0001-00"},
        follow_redirects=False,
    ).json()["data"]
    wait_for_job(client, created["id"])
    metrics_response = client.get("/api/jobs/metrics", follow_redirects=False)
    assert metrics_response.status_code == 200
    metrics = metrics_response.json()["data"]
    assert "jobs_ok" in metrics
    assert "jobs_error" in metrics
    assert "avg_duration" in metrics
    assert "last_success_at" in metrics


def test_email_notification_test_queues_job_and_logs_without_smtp(client):
    response = client.post(
        "/api/notificacoes/email/test",
        json={"recipient": "destino@empresa.com", "mensagem": "Teste operacional"},
        follow_redirects=False,
    )
    assert response.status_code == 200
    job = response.json()["data"]["job"]
    assert job["job_type"] == "email_notification"

    wait_for_job(client, job["id"])
    logs_response = client.get("/api/notificacoes/email/logs", follow_redirects=False)
    assert logs_response.status_code == 200
    logs_payload = logs_response.json()["data"]
    assert any(item["mode"] in {"log_only", "skipped"} for item in logs_payload)


def test_manual_alert_creation_queues_email_notification(client):
    recipient = client.post(
        "/api/alerts/recipients",
        json={
            "name": "Fiscal",
            "email": "fiscal@empresa.com",
            "ativo": True,
            "notify_email": True,
            "tipos_alerta": ["alerta"],
            "prioridade_minima": "alta",
        },
        follow_redirects=False,
    )
    assert recipient.status_code == 200

    response = client.post(
        "/api/alertas",
        json={
            "titulo": "Alerta manual",
            "descricao": "Criado diretamente na colecao de alertas",
            "prioridade": "alta",
            "empresa_id": "empresa-1",
        },
        follow_redirects=False,
    )
    assert response.status_code == 200
    created = response.json()["data"]
    assert created["prioridade"] == "alta"

    jobs = client.get("/api/jobs", params={"job_type": "notification_dispatch"}, follow_redirects=False).json()["data"]
    assert jobs
    wait_for_job(client, jobs[0]["id"])

    logs = client.get("/api/notificacoes/logs", follow_redirects=False).json()["data"]
    assert any(
        item["tipo"] == "alerta"
        and item["channel"] == "email"
        and item["recipient_masked"].startswith("fi***")
        and item["payload_hash"]
        and item["idempotency_key"]
        and "duration_ms" in item
        and item["attempts"] == 1
        for item in logs
    )


def test_multichannel_notification_preferences_and_test_log_without_config(client):
    preferences_response = client.put(
        "/api/notificacoes/preferences",
        json={
            "preferences": [
                {
                    "name": "Fiscal",
                    "email": "fiscal@empresa.com",
                    "whatsapp": "+5511999999999",
                    "ativo": True,
                    "channels": ["email", "whatsapp", "teams", "slack"],
                    "tipos_alerta": ["alerta", "evento"],
                    "prioridade_minima": "alta",
                    "horario_inicio": "00:00",
                    "horario_fim": "23:59",
                }
            ]
        },
        follow_redirects=False,
    )
    assert preferences_response.status_code == 200
    assert preferences_response.json()["data"][0]["channels"] == ["email", "whatsapp", "teams", "slack"]

    test_response = client.post(
        "/api/notificacoes/test",
        json={"channel": "whatsapp", "whatsapp": "+5511888888888", "mensagem": "Teste WhatsApp"},
        follow_redirects=False,
    )
    assert test_response.status_code == 200
    job = test_response.json()["data"]["job"]
    assert job["job_type"] == "notification_dispatch"
    wait_for_job(client, job["id"])

    logs = client.get("/api/notificacoes/logs", params={"channel": "whatsapp"}, follow_redirects=False).json()["data"]
    assert any(
        item["status"] == "log_only"
        and item["mode"] == "log_only"
        and item["reason"] == "whatsapp_not_configured"
        and item["recipient_masked"].startswith("***")
        for item in logs
    )

    metrics = client.get("/api/notificacoes/metrics", follow_redirects=False).json()["data"]
    assert "total_enviados" in metrics
    assert "total_erros" in metrics
    assert "total_retrying" in metrics
    assert "total_log_only" in metrics
    assert "taxa_sucesso" in metrics
    assert "tempo_medio_envio_ms" in metrics
    assert "canais_ativos" in metrics
    assert "ultimos_erros" in metrics


def test_configured_whatsapp_channel_sends(monkeypatch):
    from backend.services.channels.whatsapp_channel import WhatsAppChannel
    import backend.services.channels.whatsapp_channel as whatsapp_module

    monkeypatch.setenv("WHATSAPP_API_URL", "https://whatsapp.example/messages")
    monkeypatch.setenv("WHATSAPP_TOKEN", "secret-token")
    monkeypatch.setattr(whatsapp_module, "post_json", lambda url, payload, headers=None: {"ok": True, "status_code": 200})

    result = WhatsAppChannel().send({"mensagem": "Teste"}, ["+5511999999999"])
    assert result["sent"] is True
    assert result["mode"] == "http"


def test_notification_dispatch_idempotency_prevents_duplicate_send(monkeypatch):
    from backend.services import notification_service

    db = make_db()
    sent = {"count": 0}

    def fake_send(notification, targets):
        sent["count"] += 1
        return {"channel": "email", "sent": True, "mode": "smtp", "reason": None, "targets": targets}

    monkeypatch.setattr(notification_service.CHANNELS["email"], "send", fake_send)
    notification = {
        "subject": "Alerta critico",
        "targets": {"email": ["fiscal@empresa.com"]},
        "tipo": "alerta",
        "prioridade": "critica",
        "mensagem": "Evento critico",
        "source_id": "event-001",
    }

    first = notification_service.dispatch_notification(db, "job-1", notification)
    second = notification_service.dispatch_notification(db, "job-2", notification)

    assert sent["count"] == 1
    assert first["channels"][0]["status"] == "success"
    assert second["channels"][0]["status"] == "skipped"
    assert second["channels"][0]["reason"] == "duplicate_success"


def test_notification_retry_and_internal_alert_after_repeated_failure(monkeypatch):
    from backend.services import notification_service

    db = make_db()

    def failing_send(notification, targets):
        return {"channel": "whatsapp", "sent": False, "mode": "http", "reason": "delivery_failed", "targets": targets}

    monkeypatch.setattr(notification_service.CHANNELS["whatsapp"], "send", failing_send)
    notification = {
        "subject": "Alerta critico",
        "targets": {"whatsapp": ["+5511999999999"]},
        "tipo": "alerta",
        "prioridade": "critica",
        "mensagem": "Evento critico",
        "source_id": "event-002",
    }

    first = notification_service.dispatch_notification(db, "job-1", notification)
    second = notification_service.dispatch_notification(db, "job-1", notification)
    third = notification_service.dispatch_notification(db, "job-1", notification)

    assert first["retrying"]
    assert second["retrying"]
    assert third["errors"]
    logs = list(db["notification_logs"].find({"channel": "whatsapp"}))
    assert [item["attempts"] for item in logs] == [1, 2, 3]
    assert logs[0]["next_retry_at"]
    assert logs[-1]["status"] == "error"
    assert db["pipeline_events"].count_documents({"origem": "notifications", "severidade": "critica"}) == 1
    assert db["alertas"].count_documents({"prioridade": "critica"}) >= 1


def test_notification_rate_limit_retries(monkeypatch):
    from backend.services import notification_service

    db = make_db()
    monkeypatch.setenv("NOTIFICATION_EMAIL_RATE_PER_MIN", "1")
    db["notification_logs"].insert_one(
        {
            "channel": "email",
            "status": "success",
            "created_at": notification_service.now(),
            "duration_ms": 10,
        }
    )
    notification = {
        "subject": "Alerta",
        "targets": {"email": ["fiscal@empresa.com"]},
        "tipo": "alerta",
        "prioridade": "alta",
        "mensagem": "Evento",
        "source_id": "event-003",
    }

    result = notification_service.dispatch_notification(db, "job-1", notification)
    assert result["retrying"]
    log = db["notification_logs"].find_one({"reason": "rate_limited"})
    assert log["status"] == "retrying"
    assert log["next_retry_at"]


def test_dashboard_contains_notification_metrics(client):
    response = client.get("/api/dashboard", follow_redirects=False)
    assert response.status_code == 200
    payload = response.json()["data"]
    assert "notificacoesEnviadasHoje" in payload
    assert "notificacoesFalhasHoje" in payload
    assert "notificacoesTaxaSucesso" in payload


def test_worker_requeues_notification_dispatch_retry(client, monkeypatch):
    from backend.services import notification_service
    import backend.workers.async_jobs as async_jobs

    def failing_send(notification, targets):
        return {"channel": "whatsapp", "sent": False, "mode": "http", "reason": "delivery_failed", "targets": targets}

    monkeypatch.setattr(notification_service.CHANNELS["whatsapp"], "send", failing_send)
    monkeypatch.setattr(async_jobs, "enqueue_job", lambda job_id: None)
    inserted = app_module.db["jobs"].insert_one(
        {
            "job_type": "notification_dispatch",
            "status": "pending",
            "attempts": 0,
            "max_attempts": 3,
            "payload": {
                "notification": {
                    "subject": "Alerta",
                    "targets": {"whatsapp": ["+5511999999999"]},
                    "tipo": "alerta",
                    "prioridade": "alta",
                    "mensagem": "Evento",
                    "source_id": "worker-retry-001",
                }
            },
            "created_at": app_module.now(),
            "updated_at": app_module.now(),
        }
    )

    result = async_jobs.process_job(str(inserted.inserted_id))
    assert result["status"] == "pending"
    assert result["attempts"] == 2
    assert result["next_retry_at"]


def test_realtime_notifications_flow(client):
    empresa_id = str(app_module.db["empresas"].items[0]["_id"])
    before_dashboard = client.get("/api/dashboard", follow_redirects=False).json()["data"]
    before_events = before_dashboard["eventos_total"]
    before_alertas = before_dashboard["alertas"]

    with client.websocket_connect("/ws/notificacoes") as ws:
        response = client.post(
            "/api/events",
            json={
                "origem": "fiscal",
                "tipo": "vencimento",
                "empresa_id": empresa_id,
                "severidade": "critica",
                "titulo": "Certidao vencendo",
                "descricao": "Certidao fiscal vence hoje",
                "payload": {"empresa_id": empresa_id, "origem": "fiscal"},
                "referencia": f"rt-{ObjectId()}",
            },
            follow_redirects=False,
        )
        assert response.status_code == 200
        created = response.json()["data"]
        assert created["severidade"] == "critica"

        mensagens = [ws.receive_json(), ws.receive_json()]
        tipos = {msg["tipo"] for msg in mensagens}
        severidades = {msg["severidade"] for msg in mensagens}
        assert "evento" in tipos
        assert "alerta" in tipos
        assert severidades == {"critica"}
        assert all(msg["empresa_id"] == empresa_id for msg in mensagens)

    after_dashboard = client.get("/api/dashboard", follow_redirects=False).json()["data"]
    assert after_dashboard["eventos_total"] >= before_events + 1
    assert after_dashboard["alertas"] >= before_alertas + 1

    alertas_response = client.get("/api/alertas", follow_redirects=False)
    assert alertas_response.status_code == 200
    alertas_payload = alertas_response.json()["data"]
    assert any(alerta["empresa_id"] == empresa_id for alerta in alertas_payload)
