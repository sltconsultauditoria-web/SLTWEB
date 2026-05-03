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
