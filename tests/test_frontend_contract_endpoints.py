import re
from pathlib import Path


API_CALL_RE = re.compile(r"\bapi\.(get|post|put|delete|patch)\(\s*([`'\"])(.+?)\2", re.DOTALL)


def _normalize_frontend_path(raw_path):
    path = raw_path.strip()
    path = re.sub(r"\$\{[^}]+\}", "{param}", path)
    path = path.split("?", 1)[0]
    if not path.startswith("/"):
        path = "/" + path
    if not path.startswith("/api/") and path != "/api":
        path = "/api" + path
    return path.rstrip("/") or "/"


def _path_to_regex(openapi_path):
    escaped = re.escape(openapi_path.rstrip("/"))
    escaped = re.sub(r"\\\{[^}]+\\\}", r"[^/]+", escaped)
    return re.compile(rf"^{escaped}/?$")


def _method_exists(openapi_paths, frontend_method, frontend_path):
    if frontend_method == "get":
        # Browser downloads can be implemented as GET even when the caller sets responseType.
        pass
    for openapi_path, operations in openapi_paths.items():
        if frontend_method not in operations:
            continue
        if _path_to_regex(openapi_path).match(frontend_path.rstrip("/")):
            return True
    return False


def _extract_frontend_api_calls():
    calls = []
    src_root = Path("frontend/src")
    for path in sorted(src_root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".js", ".jsx", ".ts", ".tsx"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for match in API_CALL_RE.finditer(text):
            raw_endpoint = match.group(3)
            line = text.count("\n", 0, match.start()) + 1
            calls.append(
                {
                    "file": str(path),
                    "line": line,
                    "method": match.group(1).lower(),
                    "endpoint": _normalize_frontend_path(raw_endpoint),
                    "raw": raw_endpoint,
                }
            )
    return calls


def test_frontend_api_calls_exist_in_local_openapi(client):
    openapi_paths = client.get("/openapi.json", follow_redirects=False).json()["paths"]
    calls = _extract_frontend_api_calls()
    assert calls, "Nenhuma chamada api.get/api.post/api.put/api.delete/api.patch encontrada em frontend/src."

    failures = []
    for call in calls:
        if not _method_exists(openapi_paths, call["method"], call["endpoint"]):
            failures.append(
                "Frontend chama endpoint que nao existe no backend: "
                f"{call['file']}:{call['line']} {call['method'].upper()} {call['endpoint']} "
                f"(origem: {call['raw']}). Sugestao: registrar rota no backend ou ajustar a chamada do frontend."
            )

    assert not failures, "\n".join(failures)


def test_frontend_contract_covers_known_critical_calls():
    calls = {(call["method"], call["endpoint"]) for call in _extract_frontend_api_calls()}
    expected = {
        ("get", "/api/usuarios/viewers"),
        ("get", "/api/obrigacoes/dashboard"),
        ("get", "/api/obrigacoes/calendario"),
        ("get", "/api/obrigacoes/catalogo"),
    }

    missing = sorted(expected - calls)
    assert not missing, f"Chamadas criticas esperadas nao encontradas no frontend: {missing}"

