# ============================================
# DESCOBRIR QUAL api.js O FRONTEND USA
# Rode dentro da pasta frontend
# ============================================

Write-Host ""
Write-Host "🔎 Procurando imports de api.js no projeto..." -ForegroundColor Cyan
Write-Host ""

# procura imports comuns
Get-ChildItem -Path .\src -Recurse -Include *.js,*.jsx,*.ts,*.tsx |
Select-String -Pattern `
"from './api'",
"from '../api'",
'from "../../api"',
'from "../../../api"',
'from "./services/api"',
'from "../services/api"',
'from "../../services/api"',
'from "../../../services/api"',
'require("./api")',
'require("../api")',
'require("./services/api")',
'require("../services/api")' |
ForEach-Object {
    Write-Host "📄 $($_.Path):$($_.LineNumber)" -ForegroundColor Yellow
    Write-Host "   $($_.Line.Trim())"
    Write-Host ""
}

Write-Host ""
Write-Host "======================================" -ForegroundColor Green
Write-Host "Resumo:" -ForegroundColor Green
Write-Host "Se aparecer './api' => usa src/api.js"
Write-Host "Se aparecer 'services/api' => usa src/services/api.js"
Write-Host "======================================"