# API Status Report

Data da verificação: 2026-05-03

## Resumo

| Endpoint | Método | Status atual | Problema | Causa provável | Correção aplicada | Prioridade |
|---|---:|---:|---|---|---|---|
| `/health` | GET | 200 | Nenhum | Banco fake de teste não expunha `name` | Ajustado teste de validação com `FakeDB.name` | Baixa |
| `/api/dashboard` | GET | 200 | Nenhum | - | Coberto em pytest com banco em memória | Baixa |
| `/api/auth/login` | POST | 200 | Nenhum | - | Coberto em pytest | Baixa |
| `/api/empresas` | GET | 200 | Nenhum | - | Coberto em pytest | Baixa |
| `/api/documentos` | GET | 200 | Nenhum | - | Coberto em pytest | Baixa |
| `/api/documentos/{id}` | DELETE | 200/204 para ID válido | 404 para exclusão válida | Rota inexistente no backend principal | Implementada exclusão com `delete_one` e 404 apenas quando o ID não existe | Alta |
| `/api/fiscal/calcular/das` | POST | 200 | 404 | Rota ausente | Implementado cálculo com `FiscalEngine` e persistência opcional em `fiscal_data` | Alta |
| `/api/fiscal/calcular/fator-r` | POST | 200 | 404 | Rota ausente | Implementado cálculo com `FiscalEngine` e persistência opcional em `fiscal_data` | Alta |
| `/api/guias` | GET | 200 | Nenhum | - | Coberto em pytest | Baixa |
| `/api/obrigacoes` | GET | 200 | Nenhum | - | Coberto em pytest | Baixa |
| `/api/alertas` | GET | 200 | Nenhum | Contrato antigo inconsistente | Normalização de `prioridade`, `status`, `lido`, `resolvido`, `data` | Média |
| `/api/auditoria` | GET | 200 | Nenhum | - | Coberto em pytest | Baixa |
| `/api/auditoria/estatisticas` | GET | 200 | Nenhum | - | Coberto em pytest | Baixa |
| `/api/ocr/documentos` | GET | 200 | Nenhum | - | Coberto em pytest | Baixa |
| `/api/ocr/estatisticas` | GET | 200 | Nenhum | - | Coberto em pytest | Baixa |
| `/api/ocr/tipos-suportados` | GET | 200 | Nenhum | - | Coberto em pytest | Baixa |
| `/api/robots/ingestion/status` | GET | 200 | Nenhum | - | Coberto em pytest | Baixa |
| `/api/robots/ingestion/history?limit=10` | GET | 200 | Nenhum | - | Coberto em pytest | Baixa |
| `/api/robots/ingestion/files?limit=20` | GET | 200 | Nenhum | - | Coberto em pytest | Baixa |
| `/api/sharepoint/status` | GET | 200 | Nenhum | - | Coberto em pytest | Baixa |
| `/api/relatorios` | GET | 200 | Nenhum | - | Coberto em pytest | Baixa |
| `/api/tipos_relatorios` | GET | 200 | Nenhum | - | Coberto em pytest | Baixa |
| `/api/certidoes?cnpj=12345678000100` | GET | 200 | Nenhum | - | Coberto em pytest | Baixa |
| `/api/debitos?cnpj=12345678000100` | GET | 200 | Nenhum | - | Coberto em pytest | Baixa |

## Ajustes de frontend feitos para reduzir 307

Chamadas com barra final foram removidas nos seguintes pontos:

- `frontend/src/components/NotificationBell.jsx`
- `frontend/src/pages/Alertas.jsx`
- `frontend/src/pages/Auditoria.jsx`
- `frontend/src/pages/Certidoes.jsx`
- `frontend/src/pages/Debitos.jsx`
- `frontend/src/pages/Documentos.jsx`
- `frontend/src/pages/Guias.jsx`
- `frontend/src/pages/Obrigacoes.jsx`
- `frontend/src/pages/Relatorios.jsx`
- `frontend/src/pages/RelatoriosPersistente.jsx`

## Validação executada

- `python -m py_compile backend/main_enterprise.py tests/test_api_endpoints.py`
- `python -m pytest -v tests/test_api_endpoints.py`

Resultado:

- 26 testes executados
- 26 testes aprovados

## Endpoints pendentes

Nenhum endpoint principal ficou pendente dentro do escopo desta verificação.
