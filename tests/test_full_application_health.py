CRITICAL_OPENAPI_PATHS = [
    "/api/usuarios/viewers",
    "/api/obrigacoes/dashboard",
    "/api/obrigacoes/calendario",
    "/api/obrigacoes/catalogo",
    "/api/sped/status",
    "/api/auditoria/executar",
    "/api/documentos/{item_id}/download",
]


def test_root_health_openapi_and_docs_are_available(client):
    expected_200 = ["/", "/health", "/api/health_check/", "/openapi.json", "/docs"]

    for path in expected_200:
        response = client.get(path, follow_redirects=False)
        assert response.status_code == 200, f"{path} deveria retornar 200, retornou {response.status_code}: {response.text}"


def test_openapi_contains_critical_routes_from_health_suite(client):
    openapi = client.get("/openapi.json", follow_redirects=False).json()
    paths = openapi["paths"]
    missing = [path for path in CRITICAL_OPENAPI_PATHS if path not in paths]

    assert not missing, (
        "OpenAPI local incompleto. Rotas ausentes: "
        f"{missing}. Possivel router nao registrado em backend/main_enterprise.py "
        "ou rota faltando no modulo backend/routers correspondente."
    )

