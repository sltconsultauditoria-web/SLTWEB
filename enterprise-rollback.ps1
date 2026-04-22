# ===============================
# Enterprise Rollback Script
# consultSLTweb -> consultSLT_web
# ===============================

$Source = "C:\Users\admin-local\ServerApp\consultSLTweb"
$Target = "C:\Users\admin-local\ServerApp\consultSLT_web"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Enterprise Rollback - START" -ForegroundColor Cyan
Write-Host "========================================"
Write-Host "Source : $Source"
Write-Host "Target : $Target"
Write-Host ""

# Validações básicas
if (!(Test-Path $Source)) {
    Write-Host "❌ Diretório de origem não encontrado" -ForegroundColor Red
    exit 1
}

if (!(Test-Path $Target)) {
    Write-Host "❌ Diretório de destino não encontrado" -ForegroundColor Red
    exit 1
}

Write-Host "↩️ Revertendo alterações..." -ForegroundColor Yellow

robocopy `
    $Source `
    $Target `
    /MIR `
    /FFT `
    /Z `
    /XA:H `
    /W:2 `
    /R:2 `
    /NFL `
    /NDL `
    /NP `
    /LOG+:rollback.log

Write-Host ""
Write-Host "✅ Rollback concluído com sucesso" -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Enterprise Rollback - END" -ForegroundColor Cyan
Write-Host "========================================"
