# Render Failure Diagnosis

## STATUS

PARCIAL

## CAUSA_RAIZ

O backend tem inconsistencia de variavel de Mongo entre os modulos:
- `backend/main_enterprise.py` usa `MONGO_URI`/`MONGO_URL`
- `backend/core/database.py` usa apenas `MONGO_URL`
- `backend/middleware/auth.py` usa `MONGO_URI`/`MONGO_URL`

Se o Render estiver configurado somente com `MONGO_URI`, a camada que usa `backend/core/database.py` pode cair para o default local ou falhar no startup. Isso explica um crash com `Exited with status 1` ou um bootstrap incompleto.

## ERRO_EXATO_DO_LOG

Nao foi possivel capturar o log do Render neste workspace. O sintoma observado e `Exited with status 1` apos `uvicorn backend.main_enterprise:app --host 0.0.0.0 --port $PORT`.

## VARIAVEIS_CORRIGIDAS

- `ENV=production`
- `APP_ENV=production`
- `DB_NAME=consultslt_db`
- `CORS_ORIGINS=https://sltconsultauditoria-web.github.io`
- `FRONTEND_URL=https://sltconsultauditoria-web.github.io`
- `ASYNC_USE_REDIS=0`

## VARIAVEIS_A_REVISAR_NO_RENDER

- `MONGO_URI`
- `MONGO_URL` (se usada em algum modulo)
- `JWT_SECRET`
- `SECRET_KEY`

## ARQUIVOS_ALTERADOS

- `render.yaml`
- `GITHUB_PAGES_RENDER_INTEGRATION_REPORT.md`

## COMANDO_RENDER

- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn backend.main_enterprise:app --host 0.0.0.0 --port $PORT`
- A acao correta no Render e: `Manual Deploy -> Clear build cache and deploy`

## HEALTHCHECK

Esperado: `https://sltweb.onrender.com/health` -> HTTP 200 com JSON de health.

## PENDENCIAS

1. Confirmar nos logs do Render a linha final real do crash.
2. Unificar `MONGO_URI`/`MONGO_URL` no backend.
3. Confirmar `JWT_SECRET` forte e `SECRET_KEY` espelhado, se necessario.
4. Rodar deploy limpo no Render.
5. Validar `/health` com 200.
