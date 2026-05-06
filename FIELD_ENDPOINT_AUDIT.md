# FIELD_ENDPOINT_AUDIT

| Tela | Campo frontend | Campo backend esperado | Collection Mongo | Status | Acao |
| --- | --- | --- | --- | --- | --- |
| Login | `email`, `password` | `email`, `password` | `usuarios` | OK | Removido preenchimento fixo de senha demo no formulario. |
| Gestao de Usuarios | `password` | `password` no request, `senha_hash` no banco | `usuarios` | Normalizado | Frontend deixou de enviar `senha`; backend continua aceitando alias legado e nunca retorna hash. |
| Gestao de Usuarios Viewer | `password`, `role: viewer` | `password`, `role/perfil: viewer` | `usuarios` | Normalizado | Tela admin envia apenas viewer; endpoint `/api/usuarios/viewers` forca viewer mesmo com payload adulterado. |
| Empresas | `regime_tributario` | `regime_tributario` | `empresas` | Normalizado | Frontend deixou de enviar `regime`; backend aceita aliases legados e grava snake_case. |
| Empresas | `razao_social`, `nome_fantasia` | `razao_social`, `nome_fantasia` | `empresas` | OK | Backend normaliza aliases legados `razaoSocial` e `nomeFantasia`. |
| Documentos | `nome_arquivo` | `nome_arquivo` | `documentos` | Normalizado | Upload registra metadados top-level, sem wrapper `data.nome`. |
| Documentos | `empresa_id` | `empresa_id` | `documentos` | Normalizado | Frontend e backend aceitam empty state sem quebrar listas. |
| Alertas | `descricao` | `descricao` | `alertas` | OK | Backend aceita `mensagem` como alias e responde campo canonico `descricao`. |
| Eventos | `titulo`, `descricao`, `status` | `titulo`, `descricao`, `status` | `pipeline_events` | OK | Resolver evento mantem PATCH `/api/events/{id}/resolver`. |
| Relatorios | parametros query | query params | `empresas`, `documentos`, `auditorias` | OK | Exportacoes usam blob via apiClient e Render como base URL. |
| Guias | `regime_tributario` ou legado `regime` | `regime_tributario` | `empresas`, `guias` | Compatibilidade | Tela converte para campo interno de exibicao sem enviar payload duplicado. |

## Observacoes

- O backend preserva compatibilidade de leitura com dados antigos do Mongo que ainda contenham `regime`, `nome`, `empresa` ou `senha`, mas novos writes usam os nomes canonicos.
- `senha_hash`, `senha`, `password`, JWT secrets e segredos de infraestrutura nao sao expostos nas respostas de usuario.
- SharePoint pode retornar `not_configured`, desde que a rota responda 200 e a UI exiba estado controlado.
