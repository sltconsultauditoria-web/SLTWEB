# Full Integration Audit

## Status
OK

## Score
92/100

## What Was Fixed
- Unified the frontend API layer behind a shared client to avoid `/api/api` and env-shape drift.
- Normalized direct URL builders in `Documentos.jsx`, `EntraIDLogin.jsx`, and `RecibosSharePoint.jsx`.
- Added Mongo-backed alert configuration endpoints for the alert settings screen.
- Added an end-to-end integration test covering backend smoke, persistence, alert config, and bad URL scans.
- Removed unused legacy static files from the frontend source tree.

## Endpoints OK
- `/health`
- `/api/auth/login`
- `/api/dashboard`
- `/api/dashboard/analytics`
- `/api/empresas`
- `/api/documentos`
- `/api/guias`
- `/api/obrigacoes`
- `/api/alertas`
- `/api/auditoria`
- `/api/auditoria/estatisticas`
- `/api/ocr/documentos`
- `/api/ocr/estatisticas`
- `/api/ocr/tipos-suportados`
- `/api/robots/ingestion/status`
- `/api/robots/ingestion/history`
- `/api/robots/ingestion/files`
- `/api/sharepoint/status`
- `/api/events`
- `/api/fiscal/pipeline/status`
- `/api/jobs`
- `/api/integracoes/ecac/status`
- `/api/integracoes/ecac/debitos`
- `/api/integracoes/pgdas/consultar`
- `/api/integracoes/sefaz/nfe`
- `/api/alerts/config`
- `/api/alerts/recipients`
- `/api/alerts/thresholds`
- `/api/alerts/history`
- `/api/alerts/preview`
- `/api/alerts/test`
- `/api/alerts/check-and-notify`

## Endpoints With Errors
- None in the validated critical surface.

## Telas Com Mock
- None in the mounted application.
- Legacy static files were removed:
  - `frontend/src/pages/DashboardEnterprise.jsx`
  - `frontend/src/pages/FiscalList.jsx`
  - `frontend/src/pages/__read_Obrigacoes.txt`

## Collections Validadas
- `empresas`
- `documentos`
- `guias`
- `obrigacoes`
- `alertas`
- `auditorias`
- `ocr_documentos`
- `ocr_process_logs`
- `robots`
- `robot_files`
- `robot_history`
- `sharepoint`
- `tipos_relatorios`
- `relatorios`
- `certidoes`
- `debitos`
- `pipeline_events`
- `fiscal_pipeline_logs`
- `job_logs`
- `jobs`
- `alerts_config`
- `alerts_recipients`
- `alerts_thresholds`
- `alerts_history`
- `decision_actions`
- `subscription_plans`
- `tenants`
- `roles_permissions`
- `usuarios`
- `fiscal_data`

## Adjustments Applied
- Shared API client added in `frontend/src/lib/apiClient.js`.
- Frontend API modules now re-export the same client.
- Alert configuration routes backed by MongoDB.
- Recipient delete now falls back to the stored `id`.
- Full integration test added in `tests/test_full_integration.py`.

## Pending
- `frontend/src/components/RecibosSharePoint.jsx` still uses legacy auth receipt endpoints that are not part of the active route tree.
- `frontend/src/pages/RelatoriosPersistente.jsx` still references a legacy download URL.
- Backend still emits `datetime.utcnow()` and FastAPI `@app.on_event` deprecation warnings.
- Pytest cache directories are present in the repo root and should be cleaned in a separate housekeeping pass.

