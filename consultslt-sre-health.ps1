Write-Host ""
Write-Host "====================================="
Write-Host "CONSULT SLT - SRE HEALTH CHECK"
Write-Host "====================================="

$ports = @{
    "Frontend React" = 3000
    "Backend API" = 8000
    "API Gateway" = 8001
    "MongoDB" = 27017
}

Write-Host ""
Write-Host "VERIFICANDO PORTAS"

foreach ($service in $ports.Keys) {

    $port = $ports[$service]

    $result = netstat -ano | Select-String ":$port"

    if ($result) {
        Write-Host "[OK] $service rodando na porta $port"
    }
    else {
        Write-Host "[ERRO] $service nao encontrado"
    }
}

Write-Host ""
Write-Host "TESTANDO BACKEND"

$endpoints = @(
    "http://localhost:8000",
    "http://localhost:8000/empresas",
    "http://localhost:8000/relatorios",
    "http://localhost:8000/obrigacoes"
)

foreach ($url in $endpoints) {

    try {
        $response = Invoke-WebRequest $url -UseBasicParsing -TimeoutSec 3
        Write-Host "[OK] $url"
    }
    catch {
        Write-Host "[FAIL] $url"
    }

}

Write-Host ""
Write-Host "TESTANDO FRONTEND"

try {

    Invoke-WebRequest "http://localhost:3000" -UseBasicParsing -TimeoutSec 3
    Write-Host "[OK] Frontend respondendo"

}
catch {

    Write-Host "[FAIL] Frontend nao respondeu"

}

Write-Host ""
Write-Host "VERIFICANDO BANCO"

$mongo = netstat -ano | Select-String ":27017"

if ($mongo) {

    Write-Host "[OK] MongoDB ativo"

}
else {

    Write-Host "[ERRO] MongoDB nao encontrado"

}

Write-Host ""
Write-Host "====================================="
Write-Host "CHECK FINALIZADO"
Write-Host "====================================="