# Changelog

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

