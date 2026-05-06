# Integrações Governamentais - Roadmap

## Status atual

- `real`: SharePoint/Microsoft Graph via OAuth2 client credentials.
- `simulado`: eCAC, PGDAS-D e SEFAZ.
- `log_only`: sincronizações sem configuração válida.
- `not_configured`: quando faltam variáveis de ambiente obrigatórias.
- `not_implemented`: transmissao SPED real ainda nao finalizada.

## Fases

### Fase 1
- Endpoints de status/consulta com autenticação e RBAC consistentes.
- Separação clara entre `real`, `simulado`, `log_only` e `not_configured`.

### Fase 2
- SharePoint Graph real.
- Persistência de arquivos e logs de sincronização.

### Fase 3
- SEFAZ com certificado ICP-Brasil, SOAP e validação por UF.

### Fase 4
- eCAC e PGDAS com revisão jurídica, Gov.br, procuração e RPA quando aplicável.

### Fase 5
- SPED: validação local, geração de arquivo e transmissão oficial com PVA/certificado.

### Fase 6
- Observabilidade, auditoria e trilha de execução.

