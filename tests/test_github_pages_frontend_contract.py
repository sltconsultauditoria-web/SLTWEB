from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT / "frontend"
BUILD = FRONTEND / "build"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_api_client_uses_render_fallback_and_no_relative_api():
    api_client = read_text(FRONTEND / "src" / "lib" / "apiClient.js")

    assert 'const API_URL =' in api_client
    assert 'process.env.REACT_APP_API_URL || "https://sltweb.onrender.com/api"' in api_client
    assert 'baseURL: API_URL' in api_client
    assert 'console.log("API BASE URL:", API_URL)' in api_client
    assert 'throw new Error("REACT_APP_API_URL não configurado em produção")' not in api_client
    assert "window.location.origin" not in api_client
    assert "REACT_APP_BACKEND_URL" not in api_client
    assert 'baseURL: "/api"' not in api_client
    assert "baseURL: '/api'" not in api_client
    assert "localhost" not in api_client
    assert "shouldPrefixApiPath" not in api_client
    assert "export const resolveApiBaseUrl = () => API_URL;" in api_client


def test_auth_context_uses_api_post_login_and_no_manual_url():
    auth_context = read_text(FRONTEND / "src" / "context" / "AuthContext.jsx")

    assert 'api.post("/auth/login"' in auth_context
    assert 'fetch("/api/auth/login")' not in auth_context
    assert 'api.post("/api/auth/login"' not in auth_context
    assert 'api.get("/api/me"' not in auth_context
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


def test_frontend_source_has_no_duplicated_api_prefix_calls():
    source_files = list((FRONTEND / "src").rglob("*.js")) + list((FRONTEND / "src").rglob("*.jsx"))
    source_text = "\n".join(read_text(path) for path in source_files)

    assert "/api/me" not in source_text
    assert "/api/auth/login" not in source_text
    assert "api/api" not in source_text
    assert "window.location.origin" not in source_text
    assert "localhost:8000" not in source_text


def test_app_router_uses_sltweb_basename_and_routes():
    app_js = read_text(FRONTEND / "src" / "App.js")

    assert 'basename="/SLTWEB"' in app_js
    assert 'path="/login"' in app_js
    assert 'path="/dashboard"' in app_js
    assert 'path="/catalogo-obrigacoes"' in app_js


def test_frontend_pages_workflow_has_required_controls():
    workflow = read_text(ROOT / ".github" / "workflows" / "frontend-pages.yml")

    assert "Deploy Frontend to GitHub Pages" in workflow
    assert "workflow_dispatch" in workflow
    assert "permissions:\n  contents: write" in workflow
    assert "peaceiris/actions-gh-pages@v3" in workflow
    assert "REACT_APP_API_URL=https://sltweb.onrender.com/api \\" in workflow
    assert "PUBLIC_URL=/SLTWEB \\" in workflow
    assert "npm run build" in workflow
    assert "cp frontend/build/index.html frontend/build/404.html" in workflow
    assert "npm install" in workflow
    assert "publish_dir: ./frontend/build" in workflow
    assert "publish_branch: gh-pages" in workflow
    assert "force_orphan: true" in workflow
    assert "REACT_APP_WS_URL=wss://sltweb.onrender.com/ws/notificacoes \\" in workflow


def test_notifications_websocket_uses_configured_render_url_only():
    notifications = read_text(FRONTEND / "src" / "hooks" / "useNotifications.js")

    assert "process.env.REACT_APP_WS_URL" in notifications
    assert "window.location.host" not in notifications
    assert "window.location.protocol" not in notifications
    assert "/ws/notificacoes" not in notifications.replace(
        "REACT_APP_WS_URL=wss://sltweb.onrender.com/ws/notificacoes", ""
    )
    assert "REACT_APP_WS_URL nao configurado; usando polling de alertas." in notifications
    assert "WebSocket indisponivel; usando polling de alertas." in notifications
    assert "MAX_WEBSOCKET_FAILURES" in notifications


def test_admin_viewer_management_frontend_contract():
    app_js = read_text(FRONTEND / "src" / "App.js")
    navigation = read_text(FRONTEND / "src" / "components" / "Layout" / "navigation.js")
    configuracoes = read_text(FRONTEND / "src" / "pages" / "Configuracoes.jsx")
    page = read_text(FRONTEND / "src" / "pages" / "ConfiguracoesUsuariosViewer.jsx")
    usuarios = read_text(FRONTEND / "src" / "pages" / "Usuarios.jsx")

    assert "ConfiguracoesUsuariosViewer" not in app_js
    assert 'path="/configuracoes/usuarios-viewer"' not in app_js
    assert "<AdminRoute>" in app_js
    assert 'label: "Viewers"' not in navigation
    assert '{ icon: UserCog, label: "Viewers", path: "/configuracoes/usuarios-viewer", adminOnly: true }' not in navigation
    assert '{ path: "/configuracoes/usuarios-viewer", title: "Gest' not in navigation
    assert "isAdminUser(user)" in configuracoes
    assert "ConfiguracoesUsuariosViewer" in configuracoes
    assert "Abrir Gestao de Viewers" not in configuracoes
    assert "api.get('/usuarios/viewers')" in page
    assert "api.post('/usuarios/viewers'" in page
    assert "api.put(`/usuarios/viewers/${selectedViewer.id}`" in page
    assert "api.delete(`/usuarios/viewers/${selectedViewer.id}`" in page
    assert "role: 'viewer'" in page
    assert "payload.password = form.password" in page
    assert "payload.senha" not in page
    assert "form.senha" not in page
    assert "formData.senha" not in usuarios
    assert "password: ''" in usuarios
    assert "setForm({ ...form, role" not in page
    assert '<Navigate to="/dashboard" replace />' in page


def test_form_field_contracts_are_normalized():
    login_page = read_text(FRONTEND / "src" / "pages" / "LoginPage.jsx")
    empresas = read_text(FRONTEND / "src" / "pages" / "Empresas.jsx")
    documentos = read_text(FRONTEND / "src" / "pages" / "Documentos.jsx")
    obrigacoes = read_text(FRONTEND / "src" / "pages" / "Obrigacoes.jsx")
    catalogo = read_text(FRONTEND / "src" / "pages" / "CatalogoObrigacoes.jsx")

    assert 'useState("admin123")' not in login_page
    assert "regime_tributario" in empresas
    assert "api.post('/empresas', payload)" in empresas
    assert "regime: 'simples'" not in empresas
    assert "console.log('Dados enviados:'" not in empresas
    assert "console.log('Resposta do backend:'" not in empresas

    assert "nome_arquivo: file.name" in documentos
    assert "empresa_id: ''" in documentos
    assert "api.post('/documentos', payload)" in documentos
    assert "data: {" not in documentos
    assert "/obrigacoes/dashboard" in obrigacoes
    assert "/obrigacoes/calendario" in obrigacoes
    assert "/obrigacoes/catalogo" in catalogo
    assert "Catálogo Fiscal" in catalogo


def test_relatorios_frontend_uses_api_client_and_blob_exports():
    relatorios = read_text(FRONTEND / "src" / "pages" / "Relatorios.jsx")
    relatorios_persistente = read_text(FRONTEND / "src" / "pages" / "RelatoriosPersistente.jsx")

    assert "api.get('/tipos_relatorios')" in relatorios
    assert "api.get('/relatorios')" in relatorios
    assert "api.get(`/relatorios/export/${format}`" in relatorios
    assert "responseType: 'blob'" in relatorios
    assert "window.URL.createObjectURL" in relatorios
    assert "window.open" not in relatorios
    assert "/api/relatorios" not in relatorios
    assert "/api/api" not in relatorios
    assert "github.io/api" not in relatorios
    assert "window.location.origin" not in relatorios
    assert "window.open" not in relatorios_persistente
    assert "api.get('/relatorios/export/pdf'" in relatorios_persistente


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
    assert "/api/api" not in bundle_text
    assert "window.location.origin" not in bundle_text
