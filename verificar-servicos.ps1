Write-Host ""
Write-Host "SRE ARCHITECTURE CHECK"
Write-Host "======================="

# Verificar MongoDB
Write-Host ""
Write-Host "Verificando MongoDB..."

$mongo = netstat -ano | Select-String ":27017"

if ($mongo) {
    Write-Host "[OK] MongoDB ativo na porta 27017"
}
else {
    Write-Host "[ERRO] MongoDB nao esta rodando"
}

# Verificar Backend
Write-Host ""
Write-Host "Verificando Backend API..."

try {
    $response = Invoke-WebRequest "http://localhost:8000/docs" -UseBasicParsing -TimeoutSec 5
    Write-Host "[OK] Backend FastAPI respondendo"
}
catch {
    Write-Host "[ERRO] Backend nao respondeu"
}

# Verificar Frontend
Write-Host ""
Write-Host "Verificando Frontend..."

try {
    $response = Invoke-WebRequest "http://localhost:3000" -UseBasicParsing -TimeoutSec 5
    Write-Host "[OK] Frontend respondendo"
}
catch {
    Write-Host "[ERRO] Frontend nao respondeu"
}

# Verificar API Gateway
Write-Host ""
Write-Host "Verificando API Gateway..."

$gateway = netstat -ano | Select-String ":8080"

if ($gateway) {
    Write-Host "[OK] Gateway ativo na porta 8080"
}
else {
    Write-Host "[AVISO] Gateway nao encontrado"
}

Write-Host ""
Write-Host "CHECK FINALIZADO"