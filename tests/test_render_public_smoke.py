import os

import httpx
import pytest


pytestmark = pytest.mark.integration

RENDER_BASE_URL = "https://sltweb.onrender.com"
CRITICAL_RENDER_PATHS = [
    "/api/usuarios/viewers",
    "/api/obrigacoes/dashboard",
    "/api/obrigacoes/calendario",
    "/api/sped/status",
    "/api/auditoria/executar",
    "/api/documentos/{item_id}/download",
]


def _render_smoke_enabled():
    return os.environ.get("RUN_RENDER_SMOKE") == "1"


@pytest.mark.skipif(not _render_smoke_enabled(), reason="RUN_RENDER_SMOKE=1 nao definido")
def test_render_health_is_publicly_available():
    response = httpx.get(f"{RENDER_BASE_URL}/health", timeout=30.0)
    assert response.status_code == 200, response.text


@pytest.mark.skipif(not _render_smoke_enabled(), reason="RUN_RENDER_SMOKE=1 nao definido")
def test_render_public_openapi_has_current_critical_routes():
    response = httpx.get(f"{RENDER_BASE_URL}/openapi.json", timeout=30.0)
    assert response.status_code == 200, response.text
    paths = response.json().get("paths", {})
    missing = [path for path in CRITICAL_RENDER_PATHS if path not in paths]

    assert not missing, (
        "Render ainda esta servindo deploy antigo. "
        "Execute Manual Deploy > Clear build cache and deploy. "
        f"Rotas ausentes no OpenAPI publico: {missing}"
    )

