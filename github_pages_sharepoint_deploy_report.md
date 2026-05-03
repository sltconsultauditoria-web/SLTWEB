# GitHub Pages + SharePoint Deploy Report

Data: 2026-05-03

Projeto origem: `C:\Users\admin-local\ServerApp\consultSLTweb`

Repositório destino: `https://github.com/sltconsultauditoria-web/SLTWEB`

URL final GitHub Pages: `https://sltconsultauditoria-web.github.io/SLTWEB/`

## Status

STATUS: PARCIAL

SCORE: 90/100

## Cópia

- O remote local já aponta para o repositório destino `SLTWEB`.
- A branch local existente é `release-auditoria`; a branch `main` também existe no repositório local.
- A cópia funcional foi preparada no workspace atual sem apagar o projeto original.
- Não foi feito push automático, porque a tarefa pediu comandos manuais caso não houvesse confirmação de permissão.

## GitHub Pages

- `frontend/package.json` usa `homepage` com a URL final do Pages.
- `frontend/src/App.js` usa `BrowserRouter basename="/SLTWEB"`.
- `frontend/.env.production.example` foi criado com `REACT_APP_API_URL` e `PUBLIC_URL=/SLTWEB`.
- Workflow criado em `.github/workflows/frontend-pages.yml`.
- O build do frontend gera saída em `frontend/build`.
- O build local confirma que o app foi assumido em `/SLTWEB/`.

## SharePoint Readiness

- O backend já possui `/api/sharepoint/status`.
- O backend já possui `/api/robots/ingestion/status`.
- O backend já possui `/api/robots/ingestion/files`.
- O backend já possui `/api/robots/ingestion/history`.
- O backend agora expõe `POST /api/sharepoint/sync` como fallback seguro.
- `backend/services/sharepoint_service.py` usa Microsoft Graph e variáveis de ambiente, sem hardcode de credenciais.
- `.env.example` passou a incluir `SHAREPOINT_SITE_URL`, `SHAREPOINT_SITE_ID`, `SHAREPOINT_DRIVE_ID`, `AZURE_TENANT_ID`, `AZURE_CLIENT_ID` e `AZURE_CLIENT_SECRET`.

## Variáveis Pendentes

- `REACT_APP_API_URL` precisa ser configurado como secret do GitHub no repositório destino.
- `AZURE_TENANT_ID` precisa ser preenchido para Graph/SharePoint.
- `AZURE_CLIENT_ID` precisa ser preenchido para Graph/SharePoint.
- `AZURE_CLIENT_SECRET` precisa ser preenchido para Graph/SharePoint.
- `SHAREPOINT_SITE_ID` precisa ser configurado no ambiente de produção.
- `SHAREPOINT_DRIVE_ID` precisa ser configurado no ambiente de produção.
- `CORS_ORIGINS` precisa apontar para `https://sltconsultauditoria-web.github.io`.

## Comandos Executados

- `git remote -v`
- `git branch --show-current`
- `python -m py_compile backend/main_enterprise.py backend/core/security.py backend/middleware/auth.py backend/workers/async_jobs.py tests/test_api_endpoints.py scripts/mongo_indexes.py`
- `python -m pytest tests -q`
- `npm.cmd run build`
- `git diff --check`

## Próximos Passos

1. Fazer `git add` e `git commit` da cópia preparada.
2. Fazer `git push origin HEAD:main`.
3. Fazer `git push origin HEAD:gh-pages` apenas se o fluxo manual for usado, ou habilitar `frontend-pages.yml` no GitHub Actions.
4. Configurar os secrets do backend público e do SharePoint no GitHub.
5. Validar os endpoints no ambiente publicado: `/health`, `/api/dashboard`, `/api/auth/login`, `/api/sharepoint/status`.
6. Validar o Pages em `https://sltconsultauditoria-web.github.io/SLTWEB/`.
