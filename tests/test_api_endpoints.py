from copy import deepcopy
import time

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
        ("GET", "/api/dashboard/analytics", {}),
        ("GET", "/api/integracoes/ecac/status", {"params": {"cnpj": "12345678000100"}}),
        ("GET", "/api/integracoes/ecac/debitos", {"params": {"cnpj": "12345678000100"}}),
        ("GET", "/api/integracoes/pgdas/consultar", {"params": {"cnpj": "12345678000100"}}),
        ("GET", "/api/integracoes/sefaz/nfe", {"params": {"cnpj": "12345678000100"}}),
        ("GET", "/api/jobs", {}),
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
        follow_redirects=False,
    )
    assert pdf_response.status_code == 200
    assert "application/pdf" in pdf_response.headers["content-type"]
    assert pdf_response.content.startswith(b"%PDF")

    excel_response = client.get(
        "/api/relatorios/export/excel",
        params={"empresa_id": empresa_id},
        follow_redirects=False,
    )
    assert excel_response.status_code == 200
    assert "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" in excel_response.headers["content-type"]
    assert excel_response.content[:2] == b"PK"


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
