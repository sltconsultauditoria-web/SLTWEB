# SLTWEB Test Report

Generated: 2026-05-06

## Status

- Local pytest: `141 passed, 3 skipped`
- Frontend build: OK (`npm.cmd run build` executed in `frontend`)
- Full script: OK with `powershell -ExecutionPolicy Bypass -File scripts/run_full_tests.ps1`
- Render smoke: `/health` OK; `/openapi.json` still missing critical routes
- Operational audit: see `RENDER_OPERATIONAL_AUDIT.md`

## Endpoints validated locally

- `/`
- `/health`
- `/api/health_check/`
- `/openapi.json`
- `/docs`
- `/api/usuarios/viewers`
- `/api/usuarios/viewers/{item_id}`
- `/api/obrigacoes`
- `/api/obrigacoes/dashboard`
- `/api/obrigacoes/calendario`
- `/api/obrigacoes/catalogo`
- `/api/sped/status`
- `/api/auditoria`
- `/api/auditoria/estatisticas`
- `/api/auditoria/{item_id}`
- `/api/auditoria/executar`
- `/api/documentos/{item_id}/download`
- Public status matrix also shows:
  - `GET /api/usuarios/viewers`: 405
  - `GET /api/obrigacoes/dashboard`: 404
  - `GET /api/obrigacoes/calendario`: 404
  - `POST /api/auditoria/executar`: 404
  - `GET /api/documentos/123/download`: 404

## Production smoke endpoints

- `https://sltweb.onrender.com/health`
- `https://sltweb.onrender.com/openapi.json`
- Critical OpenAPI paths listed in `tests/test_render_public_smoke.py`

## Endpoints absent in production Render OpenAPI

- `/api/usuarios/viewers`
- `/api/obrigacoes/dashboard`
- `/api/obrigacoes/calendario`
- `/api/sped/status`
- `/api/auditoria/executar`
- `/api/documentos/{item_id}/download`

Message returned by the smoke test:

`Render ainda esta servindo deploy antigo. Execute Manual Deploy > Clear build cache and deploy.`

## Local vs Render

- Local OpenAPI contains all critical routes.
- Render public OpenAPI does not contain the critical routes above.
- Local health/root/docs/openapi checks pass.
- Render health passes, confirming the service responds, but it appears to be serving an older backend build.

## Corrections applied

- Added `/api/health_check/` alias in `backend/main_enterprise.py`.
- Added `/api/relatorios/export/{format}` contract route for frontend calls to `/relatorios/export/${format}` while preserving the existing `/pdf` and `/excel` routes.
- Updated `render.yaml` CORS_ORIGINS to include `http://localhost:3000` alongside GitHub Pages.
- Updated PowerShell scripts to propagate failing exit codes.
- Added `RENDER_OPERATIONAL_AUDIT.md`.
- Added pytest coverage for local health, OpenAPI contract, auth/RBAC, viewers, obrigacoes, auditoria, document download, CORS, serialization, frontend/backend contract, and optional Render smoke.
- Added PowerShell scripts:
  - `scripts/run_full_tests.ps1`
  - `scripts/run_render_smoke.ps1`

## Pending

- Execute Render Manual Deploy > Clear build cache and deploy.
- Re-run optional production smoke:
  - PowerShell: `$env:RUN_RENDER_SMOKE="1"; python -m pytest tests/test_render_public_smoke.py -q`
  - Expected after updated deploy: `2 passed`
