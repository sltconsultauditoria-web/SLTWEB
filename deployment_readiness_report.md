# Deployment Readiness Report

Data: 2026-05-03

Projeto: `C:\Users\admin-local\ServerApp\consultSLTweb`

## Status Executivo

STATUS: PARCIAL

SCORE: 88/100

PRONTO PARA GITHUB PAGES: SIM, condicionado ao secret `REACT_APP_API_URL`

PRONTO PARA BACKEND PRODUÇÃO: PARCIAL, código/config prontos e deployment pendente

PRONTO PARA MONGODB PERSISTENTE: PARCIAL, Docker/manifest/scripts prontos e teste real pendente

PRONTO PARA INGRESS: PARCIAL, manifest criado e aplicação em cluster pendente

Observação sobre "gong": não foi encontrada configuração, arquivo ou produto chamado `gong`. A implementação seguiu com Ingress/Gateway.

## Implementado Nesta Rodada

- Backup local criado em `backup_pre_readiness_20260503_174919`.
- `frontend/package.json` ajustado para `homepage=/SLTWEB`.
- React Router passou a usar `BrowserRouter basename={process.env.PUBLIC_URL}`.
- Redirect absoluto de login ajustado para respeitar `PUBLIC_URL`.
- `.env.production.example` criado para o frontend com `REACT_APP_API_URL`.
- CORS do FastAPI passou a ser configurável por `CORS_ORIGINS`/`FRONTEND_ORIGIN`.
- `MONGO_URI` passou a ser aceito como alias de `MONGO_URL`.
- `JWT_SECRET` passou a ter prioridade sobre `SECRET_KEY`.
- Modo produção exige JWT/secret forte em `main_enterprise.py`, `core/security.py` e `middleware/auth.py`.
- `/api/health` criado, reaproveitando `/health`.
- `/health` agora reporta Mongo, Redis e configuração do worker sem expor secrets.
- `docker-compose.yml` passou a persistir Redis com `redis_data`.
- `env_file .env` ficou opcional para manter execução local sem versionar `.env`.
- `docker-compose.prod.yml` criado com healthchecks, backend, frontend, worker, Mongo e Redis.
- Workflows GitHub Actions criados:
  - `.github/workflows/frontend-pages.yml`
  - `.github/workflows/backend-ci.yml`
  - `.github/workflows/docker-build.yml`
- Manifests Kubernetes/GKE criados em `deploy/k8s/`.
- Scripts Mongo criados:
  - `scripts/mongo_backup.ps1`
  - `scripts/mongo_restore.ps1`
  - `scripts/mongo_indexes.py`
- Teste real condicionado criado em `tests/test_real_persistence.py`.

## Workflows Criados

- `frontend-pages.yml`: instala dependências, executa `npm run build` com `PUBLIC_URL=/SLTWEB` e publica `frontend/build` no GitHub Pages.
- `backend-ci.yml`: instala Python, requirements, executa `py_compile` e `pytest`.
- `docker-build.yml`: builda Dockerfile backend e frontend; push para GHCR fica manual e condicionado a `workflow_dispatch` com `push=true`.

## Manifests Criados

- `namespace.yaml`
- `configmap.yaml`
- `secrets.example.yaml`
- `mongo-pvc.yaml`
- `mongo-deployment.yaml`
- `mongo-service.yaml`
- `redis-deployment.yaml`
- `redis-service.yaml`
- `backend-deployment.yaml`
- `backend-service.yaml`
- `worker-deployment.yaml`
- `frontend-deployment.yaml`
- `ingress.yaml`

Ingress preparado para:

- `/api` -> `backend:8000`
- `/ws` -> `backend:8000`
- `/health` -> `backend:8000`
- TLS via secret `consultslt-api-tls`
- Annotations NGINX para conexões longas/WebSocket

## GitHub Pages

Status: pronto estruturalmente.

- Build estático confirmado para `/SLTWEB/`.
- Router respeita `PUBLIC_URL`.
- Workflow Pages criado.
- API deve ser configurada por GitHub Secret `REACT_APP_API_URL`.

Pendência operacional:

- Configurar o secret `REACT_APP_API_URL` no repositório GitHub com a URL pública real do backend.
- Habilitar GitHub Pages via GitHub Actions nas configurações do repositório.

## Backend Produção

Status: parcialmente pronto.

- CORS configurável por env.
- JWT forte obrigatório em produção.
- `/health` e `/api/health` reportam Mongo/Redis/worker.
- Secrets não são retornados pelos endpoints de health.
- `MONGO_URL` e `MONGO_URI` são aceitos.
- `REDIS_URL` é validado no health quando configurado.

Pendência operacional:

- Definir `APP_ENV=production`.
- Definir `JWT_SECRET` forte com 32+ caracteres.
- Definir `CORS_ORIGINS=https://sltconsultauditoria-web.github.io`.
- Implantar imagem backend e worker no ambiente real.

## MongoDB Persistente

Status: parcialmente pronto.

- Docker Compose usa `mongo_data`.
- Kubernetes possui PVC `mongo-data`.
- Scripts de backup/restore foram criados.
- Script de índices mínimos foi criado.
- Teste real condicionado foi criado.

Índices mínimos implementados em script:

- `empresas.cnpj`
- `usuarios.email`
- `documentos.empresa_id`
- `alertas.status`
- `pipeline_events.status/severidade`
- `notification_logs.idempotency_key`
- `jobs.status`

Pendência operacional:

- Executar `python scripts/mongo_indexes.py` contra o Mongo real.
- Executar `RUN_REAL_MONGO_TESTS=1 python -m pytest tests/test_real_persistence.py -q` contra `consultslt_db`.
- Validar persistência após restart do serviço real.

## Worker/Redis

Status: pronto estruturalmente.

- Docker Compose inclui Redis persistente via AOF.
- `docker-compose.prod.yml` inclui healthcheck Redis.
- Worker roda como serviço separado.
- Kubernetes possui deployment/service Redis e deployment worker.

Pendência operacional:

- Validar processamento de jobs no cluster real.
- Definir estratégia de retenção/persistência Redis conforme criticidade das filas.

## Segurança

- `.env` não é versionado.
- `.env.*` continua ignorado, com exceção explícita para `frontend/.env.production.example`.
- `secrets.example.yaml` contém apenas placeholders.
- `JWT_SECRET`/`SECRET_KEY` fracos bloqueiam produção.
- CORS deixa de ser hardcoded para `*` quando env de produção é definido.
- Health não retorna tokens, senhas ou secrets.

Observação: há placeholders antigos no repositório, como `YOUR_ANTI_CAPTCHA_KEY` e exemplos em tela/configuração. Não foram identificados secrets reais no diff desta rodada.

## Validações Executadas

- `python -m py_compile backend/main_enterprise.py backend/core/security.py backend/middleware/auth.py backend/workers/async_jobs.py tests/test_api_endpoints.py tests/test_real_persistence.py scripts/mongo_indexes.py`: OK.
- `python -m pytest tests -q`: OK, 69 passed, 1 skipped.
- `npm.cmd run build` em `frontend`: OK, build gerado para `/SLTWEB/`.
- `docker compose --env-file .env.example -f docker-compose.yml config`: OK, com warning local de acesso a `~/.docker/config.json`.
- `docker compose --env-file .env.example -f docker-compose.prod.yml config`: OK, com warning local de acesso a `~/.docker/config.json`.

## Limitações Não Eliminadas

- Nenhum backend público real foi informado, então não houve validação HTTP externa.
- O teste real de Mongo foi criado, mas ficou skipped porque `RUN_REAL_MONGO_TESTS=1` não foi definido.
- Ingress foi criado como manifesto, mas não foi aplicado em cluster GKE/Nginx real.
- TLS depende de criar o secret/certificado real.
- GitHub Pages depende de habilitação do Pages e configuração de secrets no GitHub.
- Integrações fiscais ainda podem operar em modo simulado se credenciais reais não forem configuradas.

## Próximos Passos

1. Configurar GitHub Secret `REACT_APP_API_URL`.
2. Habilitar GitHub Pages com source GitHub Actions.
3. Publicar imagens Docker ou ajustar tags nos manifests.
4. Criar secret real Kubernetes a partir de `deploy/k8s/secrets.example.yaml`.
5. Aplicar manifests em GKE/Nginx e configurar DNS/TLS.
6. Executar `python scripts/mongo_indexes.py` contra produção.
7. Executar teste real com `RUN_REAL_MONGO_TESTS=1`.
8. Validar login, `/api/health`, `/api/dashboard`, `/ws/notificacoes` e jobs no ambiente implantado.
