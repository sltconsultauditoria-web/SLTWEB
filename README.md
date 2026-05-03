# ConsultSLTweb

ConsultSLTweb é uma plataforma fiscal enterprise para operação, monitoramento e auditoria de empresas com backend FastAPI, MongoDB e frontend React/TailAdmin.

## Funcionalidades atuais

- Dashboard com KPIs fiscais, alertas e saúde fiscal
- Pipeline de eventos com persistência em MongoDB
- Pipeline fiscal recorrente com logs operacionais
- Notificações em tempo real via WebSocket com polling de fallback
- Timeline por empresa com visão 360
- Exportação de relatórios em PDF e Excel
- OCR integrado com processamento, persistência e estatísticas
- Gestão de empresas, documentos, obrigações, guias, certidões, débitos e auditoria
- RBAC básico com perfis administrativos
- Relatórios operacionais e listagem de tipos de relatório

## Integração

- Backend principal: `backend/main_enterprise.py`
- Banco: `consultslt_db`
- Frontend: `frontend/`

## Validação

- Testes: `33 passed`
- Frontend build: aprovado

## Release

- Versão: `v1.0-enterprise`

