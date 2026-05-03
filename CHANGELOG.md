# Changelog

## v1.2-enterprise-notifications

### Added

- Dispatcher multicanal para Email, WhatsApp, Microsoft Teams e Slack
- Job assincrono `notification_dispatch` para envio fora do fluxo HTTP
- Endpoint `GET /api/notificacoes/metrics`
- Metricas de notificacoes no `/api/dashboard`
- Logs enriquecidos em `notification_logs` com canal, destinatario mascarado, hash do payload, status, tentativas, duracao e chave de idempotencia
- Alerta interno automatico quando um canal falha repetidamente

### Changed

- Retry por canal e destinatario com `max_attempts=3`
- Backoff exponencial com `next_retry_at`
- Idempotencia por evento, canal e destinatario para evitar duplicidade
- Rate limit configuravel por canal
- Worker local, polling worker e Redis/RQ respeitam `next_retry_at`
- Fallback `log_only` preservado para canais sem configuracao

### Security

- Emails e telefones sao mascarados em logs
- Payloads de log usam `payload_hash`
- Secrets, tokens e webhooks nao sao expostos em respostas ou logs

### Validation

- Suite `tests/` passando
- Build frontend aprovado

## v1.0-enterprise

### Added

- Pipeline de eventos com coleção `pipeline_events`
- Pipeline fiscal recorrente com logs em `fiscal_pipeline_logs`
- WebSocket de notificações em `/ws/notificacoes`
- Timeline por empresa em `/api/empresas/{id}/timeline`
- Exportação operacional em PDF e Excel
- Dashboard atualizado com eventos, alertas e saúde fiscal
- OCR integrado com extração e persistência

### Validation

- `33` testes automatizados passando
- Frontend build aprovado

### Notes

- Polling de alertas mantido como fallback
- Rotas existentes preservadas
- Integração baseada em MongoDB real
