from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT / "frontend"
BUILD = FRONTEND / "build"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_api_client_requires_react_app_api_url():
    api_client = read_text(FRONTEND / "src" / "lib" / "apiClient.js")

    assert "if (!process.env.REACT_APP_API_URL)" in api_client
    assert 'throw new Error("REACT_APP_API_URL não configurado em produção")' in api_client
    assert "const baseURL = process.env.REACT_APP_API_URL" in api_client
    assert "baseURL," in api_client
    assert 'console.log("API BASE URL:", process.env.REACT_APP_API_URL)' in api_client
    assert "window.location.origin" not in api_client
    assert "REACT_APP_BACKEND_URL" not in api_client
    assert 'baseURL: "/api"' not in api_client
    assert "baseURL: '/api'" not in api_client
    assert "localhost" not in api_client
    assert "resolveApiBaseUrl" in api_client
    assert "shouldPrefixApiPath" in api_client
    assert "normalizedBaseURL.endsWith(\"/api\")" in api_client


def test_auth_context_uses_api_post_login_and_no_manual_url():
    auth_context = read_text(FRONTEND / "src" / "context" / "AuthContext.jsx")

    assert 'api.post("/auth/login"' in auth_context
    assert 'fetch("/api/auth/login")' not in auth_context
    assert "window.location.origin" not in auth_context
    assert "window.location.href = `${API_URL}/api/auth/login`" not in auth_context
    assert "github.io" not in auth_context
    assert "localhost" not in auth_context


def test_legacy_entraid_login_is_neutralized():
    legacy_login = read_text(FRONTEND / "src" / "components" / "EntraIDLogin.jsx")

    assert "Fluxo legado desativado" in legacy_login
    assert "window.location.href = `${API_URL}/api/auth/login`" not in legacy_login
    assert "/api/auth/login" not in legacy_login
    assert "axios.get" not in legacy_login
    assert "resolveApiBaseUrl" not in legacy_login


def test_legacy_backend_api_helper_has_no_localhost_fallback():
    legacy_api = read_text(ROOT / "backend" / "services" / "api.js")

    assert "http://localhost:8000/api" not in legacy_api
    assert "process.env.REACT_APP_API_URL" in legacy_api
    assert "process.env.API_URL" in legacy_api
    assert "API_URL não configurado" in legacy_api


def test_app_router_uses_sltweb_basename_and_routes():
    app_js = read_text(FRONTEND / "src" / "App.js")

    assert 'basename="/SLTWEB"' in app_js
    assert 'path="/login"' in app_js
    assert 'path="/dashboard"' in app_js


def test_frontend_pages_workflow_has_required_controls():
    workflow = read_text(ROOT / ".github" / "workflows" / "frontend-pages.yml")

    assert "actions/configure-pages@v5" in workflow
    assert "actions/upload-pages-artifact@v3" in workflow
    assert "actions/deploy-pages@v4" in workflow
    assert "PUBLIC_URL: /SLTWEB" in workflow
    assert "REACT_APP_API_URL: ${{ secrets.REACT_APP_API_URL }}" in workflow
    assert "ERRO: REACT_APP_API_URL não configurado" in workflow
    assert "rm -rf node_modules" in workflow
    assert "rm -rf build" in workflow
    assert "npm install" in workflow
    assert "cp build/index.html build/404.html" in workflow


def test_404_fallback_source_exists():
    fallback = FRONTEND / "public" / "404.html"
    assert fallback.exists()
    fallback_text = read_text(fallback)
    assert "/SLTWEB/" in fallback_text


def test_build_artifacts_after_frontend_build():
    if not BUILD.exists():
        pytest.skip("frontend build not generated yet")

    index_html = read_text(BUILD / "index.html")
    bundle_text = read_text(next((BUILD / "static" / "js").glob("main.*.js")))

    assert "/SLTWEB/" in index_html
    assert (BUILD / "404.html").exists()
    assert "github.io/api" not in bundle_text
    assert "sltconsultauditoria-web.github.io/api" not in bundle_text
    assert "github.io/api/auth/login" not in bundle_text
    assert "/api/auth/login" not in bundle_text
    assert "window.location.origin" not in bundle_text
