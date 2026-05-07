# Render Operational Audit

Date: 2026-05-06

## Executive Status

- Local application: validated.
- Render service public health: responding.
- Render public OpenAPI: stale.
- Production status: not aligned with local backend contract.
- Root cause from available evidence: Render is still serving an old backend deploy or the current local changes have not been committed/pushed and redeployed.

## Local Commit And Workspace

- Current local HEAD at audit start: `910edd62 Ajuste nas rotas de auditoria para incluir o ID do usuário e o tipo de operação, além de adicionar testes para verificar a funcionalidade dessas rotas. Também foram adicionados scripts para facilitar a execução dos testes e um relatório de teste detalhado.`
- Working tree: contains uncommitted final hardening changes for `backend/routers/usuarios.py`, viewer route-order tests, reports, and prior deploy support changes.
- Operational implication: Render can only deploy committed code present on `main`. The uncommitted changes in this workspace will not appear in production until committed and pushed.

## Render Configuration From Repository

Validated in `render.yaml`:

- service name: `consultsltweb-backend`
- branch: `main`
- runtime: `python`
- buildCommand: `pip install -r requirements.txt`
- startCommand: `uvicorn backend.main_enterprise:app --host 0.0.0.0 --port $PORT`
- healthCheckPath: `/health`
- autoDeploy: `true`
- PYTHON_VERSION: `3.11.11`
- CORS_ORIGINS: `https://sltconsultauditoria-web.github.io,http://localhost:3000`

## Actions Not Executable From This Session

The following require access to the Render dashboard or Render API credentials, neither of which is available in this shell session:

- Confirm actual Render service ID/repository binding.
- Confirm actual deployed commit in Render dashboard.
- Execute Manual Deploy > Clear build cache and deploy.
- Inspect Render build logs and startup logs.
- Confirm MongoDB connection from Render runtime logs.

Required manual action:

`Manual Deploy > Clear build cache and deploy`

Do not use incremental deploy for this recovery.

## Local Validation

Command:

`powershell -ExecutionPolicy Bypass -File scripts/run_full_tests.ps1`

Result:

- Pytest: `144 passed, 3 skipped`
- React build: OK

Additional targeted validation after CORS config update:

`python -m pytest tests/test_cors_and_serialization.py tests/test_openapi_contract.py -q`

Result:

- `6 passed`

Additional targeted validation after viewer anti-shadowing hardening:

`python -m pytest tests/test_viewers_endpoints.py tests/test_openapi_contract.py -q`

Result:

- `10 passed`

## Public Render Smoke

Command:

`powershell -ExecutionPolicy Bypass -File scripts/run_render_smoke.ps1`

Result:

- `GET /health`: passed
- `GET /openapi.json`: failed contract validation

Failure:

`Render ainda esta servindo deploy antigo. Execute Manual Deploy > Clear build cache and deploy. Rotas ausentes no OpenAPI publico: ['/api/usuarios/viewers', '/api/obrigacoes/dashboard', '/api/obrigacoes/calendario', '/api/sped/status', '/api/auditoria/executar', '/api/documentos/{item_id}/download']`

## Public Endpoint Matrix

Base URL: `https://sltweb.onrender.com`

| Method | Path | Status | Interpretation |
| --- | --- | ---: | --- |
| GET | `/health` | 200 | Service is alive |
| GET | `/openapi.json` | 200 | OpenAPI served, but stale |
| GET | `/api/usuarios/viewers` | 405 | Old deployment or missing method |
| GET | `/api/obrigacoes/dashboard` | 404 | Route absent in production |
| GET | `/api/obrigacoes/calendario` | 404 | Route absent in production |
| POST | `/api/auditoria/executar` | 404 | Route absent in production |
| GET | `/api/documentos/123/download` | 404 | Route absent in production |
| OPTIONS | `/api/obrigacoes/dashboard` | 200 | CORS preflight responds |

CORS public response:

- Access-Control-Allow-Origin: `https://sltconsultauditoria-web.github.io`
- Access-Control-Allow-Methods: `DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT`

## Public Swagger And Frontend Availability

- `https://sltweb.onrender.com/docs`: 200
- `https://sltconsultauditoria-web.github.io/SLTWEB/`: 200

Swagger cannot be considered contract-complete while `/openapi.json` is stale.

Frontend page is reachable, but full browser-console validation requires an interactive browser session with production login credentials. Based on the public backend matrix, frontend flows that call the missing routes will still hit 404/405 until Render is redeployed.

## MongoDB Runtime Status

Local fake DB and serialization tests pass:

- ObjectId serialization: OK
- datetime serialization: OK
- null fields: OK
- missing document `content_type`: OK
- document download fallback: OK

Production MongoDB connection cannot be confirmed from this session without Render logs or authenticated production endpoints.

## Build And Startup Log Checklist For Render

Inspect the next clear-cache deploy logs for:

- `pip install -r requirements.txt` completes successfully.
- `python-multipart`, `pymongo`, `python-jose`, `passlib[bcrypt]`, `fastapi`, and `uvicorn` are installed.
- No `ModuleNotFoundError`.
- No `PYTHONPATH` or package root import error for `backend.main_enterprise`.
- Uvicorn starts with `backend.main_enterprise:app`.
- `$PORT` is used, not a fixed port.
- No stacktrace after startup.
- MongoDB connection failures, if any, are visible and do not prevent `/health` from responding.

## Differences Local Vs Production

- Local OpenAPI contains all critical routes.
- Production OpenAPI misses six critical routes.
- Local `GET /api/usuarios/viewers` returns 401 without token, 403 with viewer token, and 200 with admin token.
- Production `GET /api/usuarios/viewers` still returns 405, which matches an old deployment where the path exists but the GET method is not registered.
- Local smoke passes except optional Render checks.
- Production smoke fails OpenAPI contract.
- Local CORS now includes GitHub Pages and localhost in `render.yaml`; production currently shows GitHub Pages only until redeploy.

## Final 405 Diagnosis

The current FastAPI runtime registers these user routes in the correct order:

- `/api/usuarios GET`
- `/api/usuarios POST`
- `/api/usuarios/viewers GET`
- `/api/usuarios/viewers POST`
- `/api/usuarios/viewers/{item_id} PUT`
- `/api/usuarios/viewers/{item_id} DELETE`
- `/api/usuarios/{item_id} PUT`
- `/api/usuarios/{item_id} DELETE`

The legacy router `backend/routers/usuarios.py` previously had the risky shape where `/{item_id}` appeared before any `/viewers` route. It has now been hardened by declaring `/viewers` and `/viewers/{item_id}` before `/{item_id}`.

Because production OpenAPI still omits `/api/usuarios/viewers` and public production returns 405 while local tests pass, the remaining production 405 is operational: Render is serving old code or a deployment that does not include the current route table.

## Required Next Steps

1. Commit and push the current workspace changes if they should be included in production.
2. In Render, run `Manual Deploy > Clear build cache and deploy`.
3. Confirm the deployed commit is `fb23783c` or a newer commit containing the current test/config changes.
4. Re-run:
   - `powershell -ExecutionPolicy Bypass -File scripts/run_full_tests.ps1`
   - `powershell -ExecutionPolicy Bypass -File scripts/run_render_smoke.ps1`
5. Re-check `https://sltweb.onrender.com/openapi.json` for all critical routes.
6. Validate frontend authenticated flows in a browser session.
