# Cleanup Plan

Data da análise: 2026-05-03

## Objetivo

Classificar a raiz do projeto em itens essenciais, apoio de QA, backups, caches temporários, legado e itens de risco. Nenhuma remoção foi executada.

## Regras aplicadas

- Manter `backend/`, `frontend/`, `tests/` e `.gitignore`
- Não remover arquivos necessários para rodar a aplicação
- Não apagar segredos ou arquivos sensíveis sem revisão
- Gerar plano antes de qualquer limpeza
- Preparar ações reversíveis com `archive/`

## Classificação

### ESSENCIAL

Arquivos e pastas necessários para a aplicação:

- `backend/`
- `frontend/`
- `tests/`
- `.gitignore`
- `frontend/package.json`
- `frontend/package-lock.json`
- `frontend/craco.config.js`
- `frontend/postcss.config.js`
- `frontend/tailwind.config.js`
- `frontend/jsconfig.json`
- `frontend/public/`
- `frontend/src/`

### DEV/QA

Itens úteis para teste, auditoria e validação:

- `tests/`
- `api_status_report.md`
- `relatorio_*.json`
- `guardian_report_after_fix.json`
- `healthcheck_correlacao.json`
- `impacto_dashboard_update.json`

### BACKUP

Itens de backup histórico:

- `_BACKUPS/`
- `_HOTFIX_BACKUP/`
- `_PATCH_BACKUP/`
- `_UPGRADE_BACKUPS/`
- `_VERSION_BACKUP/`
- `backup_precheck/`
- `backup_pre_mocks_endpoints_masks_20260502_200553/`
- `backup_pre_tailadmin_ocr_20260502_194751/`
- `backend/main_enterprise.py.bak_20260501_113934`
- `backend/main_enterprise_backup_20260501_122550.py`
- `frontend/.env.bak_20260501_113934`

### TEMP/CACHE

Seguro para remover após confirmação de uso local:

- `pytest-cache-files-*`
- `backend/__pycache__/`
- `tests/__pycache__/`
- `frontend/node_modules/`
- `frontend/build/`
- `backend/venv/`

### LEGADO

Scripts antigos de diagnóstico, patch e validação:

- `ajuste_total_consultsltweb.py`
- `analisar_impacto_integracao.py`
- `analisar_preparo_tailadmin_ocr.py`
- `backend_second_validation.py`
- `backend_second_validation_v3.py`
- `backend_second_validation_v4.py`
- `backup_total_consultsltweb.py`
- `beneficios_tailadmin_ocr.py`
- `check_frontend_routes.py`
- `corrigir_dashboard_real.py`
- `diagnostico_backend_frontend.py`
- `diagnostico_fastapi_rotas.py`
- `fix_apis_500_consultslt.py`
- `hotfix_alertas_obrigacoes_consultsltweb.py`
- `integracao_total_mongodb.py`
- `integracao_total_sltweb.py`
- `patch_final_consultsltweb.py`
- `patch_login_consultsltweb.py`
- `safe_backend_audit.py`
- `segunda_validacao_pre_ajuste.py`
- `telebranca.py`
- `upgrade_enterprise_consultsltweb.py`
- `upgrade_sem_reinventar_rotas.py`
- `upgrade_total_consultslt.py`
- `validar_hotfix_alertas_obrigacoes.py`
- `validar_patch_final_consultsltweb.py`
- `verificar_antes_alterar.py`
- `verificar_atualizacao_tailadmin_ocr.py`
- `verificar_correlacao_total.py`
- `verificar_ecossistema_total.py`
- `verificar_impacto_dashboard_update.py`
- `verificar_tailadmin_ocr_v2.py`
- `verificar_upgrade_enterprise_consultsltweb.py`

### RISCO

Itens sensíveis ou que exigem revisão antes de qualquer movimento:

- `frontend/.env`
- `frontend/.env.bak_20260501_113934`
- `.git/`
- `backend/venv/`
- `frontend/node_modules/`
- `frontend/build/`

## Impacto por item raiz

### Pode manter

- `backend/`
- `frontend/`
- `tests/`
- `.gitignore`
- `frontend/package.json`
- `frontend/package-lock.json`
- `frontend/craco.config.js`
- `frontend/postcss.config.js`
- `frontend/tailwind.config.js`
- `frontend/jsconfig.json`
- `frontend/public/`
- `frontend/src/`
- `frontend/.env`
- `api_status_report.md`

### Pode mover para `archive/`

- `_BACKUPS/`
- `_HOTFIX_BACKUP/`
- `_PATCH_BACKUP/`
- `_UPGRADE_BACKUPS/`
- `_VERSION_BACKUP/`
- `backup_precheck/`
- `backup_pre_mocks_endpoints_masks_20260502_200553/`
- `backup_pre_tailadmin_ocr_20260502_194751/`
- `relatorio_*.json`
- `guardian_report_after_fix.json`
- `healthcheck_correlacao.json`
- `impacto_dashboard_update.json`
- scripts antigos listados em `LEGADO`

### Pode remover

- `pytest-cache-files-*`
- `backend/__pycache__/`
- `tests/__pycache__/`

### Não mexer

- `.git/`
- `backend/`
- `frontend/`
- `tests/`
- `.gitignore`
- `frontend/.env`
- `frontend/package.json`
- `frontend/package-lock.json`
- `frontend/craco.config.js`
- `frontend/postcss.config.js`
- `frontend/tailwind.config.js`
- `frontend/public/`
- `frontend/src/`

## Seguro para deletar

Baixo risco, desde que exista backup e a app seja reinstalada quando necessário:

- `pytest-cache-files-*`
- `backend/__pycache__/`
- `tests/__pycache__/`

Moderado, melhor mover antes de apagar:

- `relatorio_*.json`
- `api_status_report.md`
- scripts antigos de diagnóstico e hotfix
- backups históricos duplicados com ZIP equivalente

## Proposta de archive

- `archive/backups/`
- `archive/reports/`
- `archive/scripts/`

## Comandos PowerShell seguros

Verificar alvo antes de mover:

```powershell
$target = Resolve-Path .\_VERSION_BACKUP
Write-Host $target
```

Mover backups:

```powershell
New-Item -ItemType Directory -Force archive\backups | Out-Null
Move-Item -LiteralPath .\_BACKUPS, .\_HOTFIX_BACKUP, .\_PATCH_BACKUP, .\_UPGRADE_BACKUPS, .\_VERSION_BACKUP -Destination archive\backups
```

Mover relatórios:

```powershell
New-Item -ItemType Directory -Force archive\reports | Out-Null
Move-Item -LiteralPath .\api_status_report.md, .\relatorio_*.json, .\guardian_report_after_fix.json, .\healthcheck_correlacao.json, .\impacto_dashboard_update.json -Destination archive\reports
```

Mover scripts legados:

```powershell
New-Item -ItemType Directory -Force archive\scripts | Out-Null
Move-Item -LiteralPath .\ajuste_total_consultsltweb.py, .\analisar_impacto_integracao.py, .\analisar_preparo_tailadmin_ocr.py, .\backend_second_validation.py, .\backend_second_validation_v3.py, .\backend_second_validation_v4.py, .\backup_total_consultsltweb.py, .\beneficios_tailadmin_ocr.py, .\check_frontend_routes.py, .\corrigir_dashboard_real.py, .\diagnostico_backend_frontend.py, .\diagnostico_fastapi_rotas.py, .\fix_apis_500_consultslt.py, .\hotfix_alertas_obrigacoes_consultsltweb.py, .\integracao_total_mongodb.py, .\integracao_total_sltweb.py, .\patch_final_consultsltweb.py, .\patch_login_consultsltweb.py, .\safe_backend_audit.py, .\segunda_validacao_pre_ajuste.py, .\telebranca.py, .\upgrade_enterprise_consultsltweb.py, .\upgrade_sem_reinventar_rotas.py, .\upgrade_total_consultslt.py, .\validar_hotfix_alertas_obrigacoes.py, .\validar_patch_final_consultsltweb.py, .\verificar_antes_alterar.py, .\verificar_atualizacao_tailadmin_ocr.py, .\verificar_correlacao_total.py, .\verificar_ecossistema_total.py, .\verificar_impacto_dashboard_update.py, .\verificar_tailadmin_ocr_v2.py, .\verificar_upgrade_enterprise_consultsltweb.py -Destination archive\scripts
```

Remover caches:

```powershell
Remove-Item -LiteralPath .\pytest-cache-files-* -Recurse -Force
Remove-Item -LiteralPath .\backend\__pycache__, .\tests\__pycache__ -Recurse -Force
```

## Validação depois da limpeza

- `python -m pytest -v`
- `uvicorn backend.main_enterprise:app --reload --port 8000`
- `cd frontend && npm start`

## Observação

Nada foi removido nesta etapa. O plano está pronto para revisão e confirmação antes de qualquer limpeza física.
