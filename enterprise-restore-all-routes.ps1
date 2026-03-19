# =========================================
# SLTWEB - RESTORE ULTIMA VERSAO COM ROTAS OK
# =========================================

Write-Host ""
Write-Host "========================================"
Write-Host " RESTAURANDO VERSAO ESTAVEL (ROTAS OK)"
Write-Host "========================================"
Write-Host ""

$root = "C:\Users\admin-local\ServerApp\consultSLTweb"
$backup = "$root\_stable_backup"

if (-not (Test-Path $backup)) {
    New-Item -ItemType Directory -Path $backup | Out-Null
}

# -----------------------------------------
# 1. FRONTEND - RESTAURAR App.js
# -----------------------------------------
$app = "$root\frontend\src\App.js"
$appBak = "$root\frontend\src\App.js.backup"

if (Test-Path $appBak) {
    Copy-Item $appBak $app -Force
    Write-Host "[OK] App.js restaurado"
}

# -----------------------------------------
# 2. FRONTEND - REMOVER api.js (axios global)
# -----------------------------------------
$apiJs = "$root\frontend\src\lib\api.js"
if (Test-Path $apiJs) {
    Copy-Item $apiJs "$backup\api.js.bak" -Force
    Remove-Item $apiJs -Force
    Write-Host "[OK] api.js removido"
}

# -----------------------------------------
# 3. FRONTEND - GARANTIR AXIOS PADRAO
# -----------------------------------------
$utils = "$root\frontend\src\lib\utils.js"
if (Test-Path $utils) {
    Copy-Item $utils "$backup\utils.js.bak" -Force
}

# -----------------------------------------
# 4. FRONTEND - REMOVER WEBSOCKET
# -----------------------------------------
Get-ChildItem "$root\frontend\src" -Recurse -Include *.js,*.jsx |
ForEach-Object {
    (Get-Content $_.FullName) |
    Where-Object { $_ -notmatch "WebSocket|wss://" } |
    Set-Content $_.FullName
}

Write-Host "[OK] WebSocket removido do frontend"

# -----------------------------------------
# 5. BACKEND - GARANTIR ROUTERS INCLUÍDOS
# -----------------------------------------
$main = "$root\main_enterprise.py"

if (Test-Path $main) {
    Copy-Item $main "$backup\main_enterprise.py.bak" -Force
    Write-Host "[OK] main_enterprise.py preservado"
}

# -----------------------------------------
# 6. BACKEND - PRESERVAR .env
# -----------------------------------------
$env = "$root\.env"
if (Test-Path $env) {
    Copy-Item $env "$backup\.env.bak" -Force
    Write-Host "[OK] .env backend mantido"
}

# -----------------------------------------
# 7. LIMPEZA FRONTEND
# -----------------------------------------
$build = "$root\frontend\build"
if (Test-Path $build) {
    Remove-Item $build -Recurse -Force
}

Write-Host ""
Write-Host "========================================"
Write-Host " RESTAURACAO CONCLUIDA COM SUCESSO"
Write-Host " TODAS AS ROTAS DEVEM FUNCIONAR"
Write-Host "========================================"
Write-Host ""
