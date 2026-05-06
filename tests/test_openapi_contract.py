CRITICAL_ROUTES = {
    "/api/usuarios/viewers": "backend/main_enterprise.py ou backend/routers/usuarios.py",
    "/api/obrigacoes/dashboard": "backend/main_enterprise.py ou backend/routers/obrigacoes.py",
    "/api/obrigacoes/calendario": "backend/main_enterprise.py ou backend/routers/obrigacoes.py",
    "/api/obrigacoes/catalogo": "backend/main_enterprise.py ou backend/routers/obrigacoes.py",
    "/api/sped/status": "backend/main_enterprise.py",
    "/api/auditoria/executar": "backend/main_enterprise.py ou backend/routers/auditorias.py",
    "/api/documentos/{item_id}/download": "backend/main_enterprise.py ou backend/routers/documentos.py",
}


def test_openapi_contract_has_all_critical_paths(client):
    response = client.get("/openapi.json", follow_redirects=False)
    assert response.status_code == 200
    paths = response.json()["paths"]

    missing_messages = [
        f"- rota ausente: {route}; possivel router nao registrado; arquivo provavel: {file_hint}"
        for route, file_hint in CRITICAL_ROUTES.items()
        if route not in paths
    ]

    assert not missing_messages, "OpenAPI local incompleto:\n" + "\n".join(missing_messages)


def test_openapi_contract_has_expected_methods(client):
    paths = client.get("/openapi.json", follow_redirects=False).json()["paths"]
    expected = {
        "/api/usuarios/viewers": {"get", "post"},
        "/api/usuarios/viewers/{item_id}": {"put", "delete"},
        "/api/obrigacoes/dashboard": {"get"},
        "/api/obrigacoes/calendario": {"get"},
        "/api/obrigacoes/catalogo": {"get"},
        "/api/sped/status": {"get"},
        "/api/auditoria/executar": {"post"},
        "/api/documentos/{item_id}/download": {"get"},
    }

    failures = []
    for path, methods in expected.items():
        actual = {method for method in paths.get(path, {}) if method in {"get", "post", "put", "delete", "patch"}}
        missing = methods - actual
        if missing:
            failures.append(f"{path}: metodos ausentes {sorted(missing)}; metodos encontrados {sorted(actual)}")

    assert not failures, "Metodos OpenAPI criticos ausentes:\n" + "\n".join(failures)

