# ======================================
# ENTERPRISE HEALTH CHECK - SLTWEB
# READ ONLY - NAO ALTERA NADA
# ======================================

$results = @()
$score = 0
$total = 10

function Check {
    param (
        [string]$name,
        [bool]$condition,
        [string]$fix
    )

    if ($condition) {
        $script:results += "[OK]  $name"
        $script:score++
    } else {
        $script:results += "[ERRO] $name"
        $script:results += "       CORRECAO: $fix"
    }
}

Write-Host ""
Write-Host "========================================"
Write-Host " SLTWEB - ENTERPRISE HEALTH CHECK"
Write-Host "========================================"
Write-Host ""

# 1. Frontend
Check `
    "Frontend em localhost:3000" `
    (Test-NetConnection localhost -Port 3000 -InformationLevel Quiet) `
    "Iniciar frontend (npm run dev ou npm start)"

# 2. Backend
Check `
    "Backend em localhost:8000" `
    (Test-NetConnection localhost -Port 8000 -InformationLevel Quiet) `
    "Iniciar backend (uvicorn main_enterprise:app --reload)"

# 3. CORS
$mainFile = "C:\Users\admin-local\ServerApp\consultSLTweb\backend\main_enterprise.py"
$hasCors = $false
if (Test-Path $mainFile) {
    if (Select-String -Path $mainFile -Pattern "CORSMiddleware" -Quiet) {
        $hasCors = $true
    }
}
Check `
    "CORS configurado no backend" `
    $hasCors `
    "Adicionar CORSMiddleware no main_enterprise.py"

# 4. API empresas
$apiOk = $false
try {
    $resp = Invoke-WebRequest "http://127.0.0.1:8000/api/empresas" -UseBasicParsing -TimeoutSec 5
    if ($resp.StatusCode -eq 200) { $apiOk = $true }
} catch {
    $apiOk = $false
}
Check `
    "Endpoint /api/empresas responde" `
    $apiOk `
    "Verificar router empresas e include_router"

# 5. AuthContext
$authFile = "C:\Users\admin-local\ServerApp\consultSLTweb\frontend\src\context\AuthContext.jsx"
Check `
    "AuthContext.jsx existe" `
    (Test-Path $authFile) `
    "Restaurar AuthContext.jsx"

# 6. Axios baseURL
$axiosOk = $false
if (Test-Path $authFile) {
    if (Select-String -Path $authFile -Pattern "baseURL" -Quiet) {
        $axiosOk = $true
    }
}
Check `
    "Axios baseURL configurado" `
    $axiosOk `
    "Configurar axios.defaults.baseURL"

# 7. MongoDB
Check `
    "MongoDB na porta 27017" `
    (Test-NetConnection localhost -Port 27017 -InformationLevel Quiet) `
    "Iniciar MongoDB ou verificar conexao"

# 8. Estrutura paginas
Check `
    "Frontend possui pasta pages" `
    (Test-Path "C:\Users\admin-local\ServerApp\consultSLTweb\frontend\src\pages") `
    "Restaurar estrutura frontend/pages"

# 9. WebSocket
Check `
    "WebSocket configurado" `
    $false `
    "Implementar WebSocket ou remover chamadas do frontend"

# 10. Variaveis de ambiente
Check `
    ".env carregado" `
    (Test-Path "C:\Users\admin-local\ServerApp\consultSLTweb\.env") `
    "Criar arquivo .env"

# Resultado final
$percent = [math]::Round(($score / $total) * 100, 2)

Write-Host ""
Write-Host "----------------------------------------"
$results | ForEach-Object { Write-Host $_ }
Write-Host "----------------------------------------"
Write-Host ""
Write-Host "SAUDE ATUAL DA APLICACAO: $percent %"
Write-Host ""
Write-Host "========================================"
Write-Host " FIM DO DIAGNOSTICO"
Write-Host "========================================"
