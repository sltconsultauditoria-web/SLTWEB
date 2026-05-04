# ConsultSLTweb

ConsultSLTweb e uma plataforma fiscal enterprise para operacao, monitoramento, auditoria e notificacoes de eventos fiscais, com backend FastAPI, MongoDB, workers assincronos e frontend React.

## Funcionalidades

- Dashboard com KPIs fiscais, alertas, saude fiscal e metricas de notificacoes
- Pipeline de eventos com persistencia em MongoDB (`pipeline_events`)
- Alertas fiscais derivados de eventos e obrigacoes
- Worker assincrono com jobs persistidos em MongoDB e suporte a Redis/RQ
- Notificacoes realtime via WebSocket em `/ws/notificacoes`
- Notificacoes multicanal com Email, WhatsApp, Microsoft Teams e Slack
- Timeline por empresa com visao 360
- Exportacao de relatorios em PDF e Excel
- OCR integrado com processamento, persistencia e estatisticas
- Gestao de empresas, documentos, obrigacoes, guias, certidoes, debitos e auditoria
- RBAC basico com perfis administrativos

## Notificacoes Multicanal

O dispatcher multicanal usa `alertas` e `pipeline_events` como fonte unica. Todo envio e processado de forma assincrona pelo job `notification_dispatch`; nenhum canal e chamado no fluxo sincronico da API.

Canais suportados:

- Email via SMTP/TLS
- WhatsApp via API HTTP configuravel
- Microsoft Teams via webhook
- Slack via webhook

Controles de producao:

- Retry por canal e destinatario com `max_attempts=3`
- Backoff exponencial com `next_retry_at`
- Idempotencia por evento, canal e destinatario
- Rate limit por canal
- Logs enriquecidos em `notification_logs`
- Mascaramento de email e telefone nos logs
- Fallback seguro `log_only` quando o canal nao estiver configurado
- Alerta interno quando um canal falha repetidamente

Endpoints principais:

- `GET /api/notificacoes/channels`
- `GET /api/notificacoes/preferences`
- `PUT /api/notificacoes/preferences`
- `POST /api/notificacoes/test`
- `GET /api/notificacoes/logs`
- `GET /api/notificacoes/metrics`

Metricas expostas em `/api/notificacoes/metrics`:

- `total_enviados`
- `total_erros`
- `total_retrying`
- `total_log_only`
- `taxa_sucesso`
- `canais_ativos`
- `ultimos_erros`
- `tempo_medio_envio_ms`

## Variaveis de Ambiente

Copie `.env.example` para `.env` no ambiente local/producao e preencha apenas fora do Git.

```env
SMTP_HOST=
SMTP_PORT=587
SMTP_USER=
SMTP_PASS=
SMTP_FROM=
WHATSAPP_API_URL=
WHATSAPP_TOKEN=
TEAMS_WEBHOOK_URL=
SLACK_WEBHOOK_URL=
NOTIFICATION_EMAIL_RATE_LIMIT_PER_MIN=
NOTIFICATION_WHATSAPP_RATE_LIMIT_PER_MIN=
```

Observacao: `.env` e `.env.*` sao ignorados pelo Git. Nao versionar secrets, tokens, certificados ou chaves privadas.

## Integracao

- Backend principal: `backend/main_enterprise.py`
- Servico de notificacoes: `backend/services/notification_service.py`
- Canais: `backend/services/channels/`
- Worker: `backend/workers/async_jobs.py` e `backend/worker.py`
- Banco: `consultslt_db`
- Frontend: `frontend/`

## Validacao

- Testes: `python -m pytest tests -q`
- Build frontend: `cd frontend && npm.cmd run build`

## Release

- Versao atual: `v1.2-enterprise-notifications`

## 14. Como Subir a Aplicacao Passo a Passo

### 14.1 Pre-requisitos

Antes de subir o sistema, confirme a instalacao e configuracao de:

- Python 3.11+
- Node.js e npm
- MongoDB
- Redis
- Git
- Docker e Docker Compose
- Variaveis de ambiente

Versoes e servicos podem variar entre ambiente local, homologacao e producao, mas os contratos principais devem permanecer os mesmos.

### 14.2 Subir MongoDB `consultslt_db`

1. Inicie o MongoDB localmente ou via Docker.
2. Conecte no servidor com `mongosh`.
3. Selecione o banco:

```javascript
use consultslt_db
```

4. Valide a conexao e as collections:

```javascript
show collections
```

5. Crie os indices padrao:

```bash
python scripts/mongo_indexes.py
```

6. Confirme as collections principais:

- `empresas`
- `usuarios`
- `documentos`
- `alertas`
- `pipeline_events`
- `jobs`
- `notification_logs`

Se o banco estiver vazio, o sistema pode iniciar, mas algumas telas e fluxos dependem de dados reais.

### 14.3 Subir Backend FastAPI

1. Entre na raiz do projeto.
2. Crie o ambiente virtual:

```bash
python -m venv .venv
```

3. Ative o ambiente:

```powershell
.venv\Scripts\activate
```

4. Instale as dependencias:

```bash
pip install -r requirements.txt
```

5. Crie o `.env` com as variaveis minimas:

```env
MONGO_URI=mongodb://localhost:27017/
DB_NAME=consultslt_db
JWT_SECRET=...
REDIS_URL=redis://localhost:6379
CORS_ORIGINS=http://localhost:3000,https://sltconsultauditoria-web.github.io
```

6. Suba a API:

```bash
uvicorn backend.main_enterprise:app --reload --reload-dir backend --port 8000
```

7. Valide:

- `http://localhost:8000/health`
- `http://localhost:8000/docs`

### 14.4 Subir Worker / Redis

1. Inicie o Redis localmente ou via Docker.
2. Rode o worker:

```bash
python -m backend.worker
```

3. Valide os jobs:

- `http://localhost:8000/api/jobs`
- `http://localhost:8000/api/jobs/metrics`

### 14.5 Subir Frontend React

1. Entre em `frontend`:

```bash
cd frontend
```

2. Instale as dependencias:

```bash
npm install
```

3. Crie o `.env` local:

```env
REACT_APP_API_URL=http://localhost:8000/api
PUBLIC_URL=/SLTWEB
```

4. Suba em modo local:

```bash
npm start
```

5. Acesse:

- `http://localhost:3000/SLTWEB/login`

6. Gere o build:

```bash
npm run build
```

### 14.6 Login Inicial

Credenciais iniciais conhecidas no ambiente de desenvolvimento:

- `admin@empresa.com / admin123`
- `william.lucas@sltconsult.com.br / Slt@2024`
- `admin@consultslt.com.br / Consult@2026`

Se algum login falhar, verifique seed de usuarios, hash de senha, JWT e CORS.

### 14.7 Subir com Docker Compose

1. Configure o `.env`.
2. Suba os servicos:

```bash
docker compose up -d --build
```

3. Verifique os containers:

```bash
docker compose ps
```

4. Veja logs:

```bash
docker compose logs -f backend
docker compose logs -f worker
```

5. Valide:

- `http://localhost:8000/health`
- `http://localhost:3000/SLTWEB/`

### 14.8 Deploy GitHub Pages

1. Repositorio:

```text
https://github.com/sltconsultauditoria-web/SLTWEB
```

2. URL final:

```text
https://sltconsultauditoria-web.github.io/SLTWEB/
```

3. Configure o GitHub Secret:

```text
REACT_APP_API_URL=https://URL_PUBLICA_DO_BACKEND
```

Observacao: o frontend adiciona `/api` no cliente HTTP quando necessario. O secret deve apontar para a raiz publica do backend, sem duplicar `/api`.

4. Em `Settings -> Pages`, selecione `Source: GitHub Actions`.
5. Rode o workflow `frontend-pages.yml`.
6. Valide:

- `/SLTWEB/`
- `/SLTWEB/login`
- `/SLTWEB/dashboard`

Observacao: o Pages hospeda apenas o frontend estatico. O backend precisa estar em uma URL publica separada.

### 14.9 Checklist de Validacao

Rode, na ordem:

```bash
python -m pytest tests -q
cd frontend && npm run build
curl http://localhost:8000/health
curl http://localhost:8000/api/dashboard
```

Depois valide manualmente:

- login
- dashboard
- MongoDB
- SharePoint
- WebSocket
- notificacoes

### 14.10 Troubleshooting

- Erro 405 no login: confira `REACT_APP_API_URL` no build e no secret do GitHub.
- GitHub Pages 404: use `/SLTWEB/` e confirme o `404.html` no build.
- MongoDB nao conecta: valide `MONGO_URI` e o banco `consultslt_db`.
- CORS bloqueado: ajuste `CORS_ORIGINS`.
- Worker nao processa: valide Redis e o processo do worker.
- WebSocket nao conecta: valide `/ws/notificacoes` e o proxy/ingress.
