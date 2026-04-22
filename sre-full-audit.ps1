Write-Host ""
Write-Host "========================================="
Write-Host "CONSULT SLT - FULL SRE ARCHITECTURE AUDIT"
Write-Host "========================================="

$root = Get-Location

# arquivos de saída
$treeFile = "sre-tree.txt"
$routeFile = "sre-routes.txt"
$testFile = "sre-endpoint-test.txt"
$reportFile = "sre-architecture-report.txt"

Write-Host ""
Write-Host "1) GERANDO TREE DA APLICACAO..."

cmd /c tree /F /A > $treeFile

Write-Host "OK -> $treeFile"

# =========================
# DESCOBRIR ROTAS
# =========================

Write-Host ""
Write-Host "2) DESCOBRINDO ROTAS DA API..."

$routes = @()

$files = Get-ChildItem -Recurse -Include *.js,*.ts,*.py

foreach ($file in $files) {

    $content = Get-Content $file.FullName

    foreach ($line in $content) {

        if ($line -match "/api/[a-zA-Z0-9/_-]+") {

            $endpoint = $matches[0]

            if ($routes -notcontains $endpoint) {

                $routes += $endpoint

            }

        }

    }

}

$routes | Out-File $routeFile

Write-Host "OK -> $routeFile"

# =========================
# TESTAR ENDPOINTS
# =========================

Write-Host ""
Write-Host "3) TESTANDO ENDPOINTS..."

$results = @()

foreach ($route in $routes) {

    $url = "http://localhost:8000$route"

    try {

        $response = Invoke-WebRequest $url -UseBasicParsing -TimeoutSec 3

        $status = $response.StatusCode

        $msg = "$route -> $status"

        Write-Host "[OK] $msg"

        $results += $msg

    }
    catch {

        if ($_.Exception.Response) {

            $status = $_.Exception.Response.StatusCode.value__

            $msg = "$route -> $status"

        }
        else {

            $msg = "$route -> NO RESPONSE"

        }

        Write-Host "[FAIL] $msg"

        $results += $msg

    }

}

$results | Out-File $testFile

Write-Host "OK -> $testFile"

# =========================
# VERIFICAR MONGODB
# =========================

Write-Host ""
Write-Host "4) VERIFICANDO MONGODB..."

$mongo = netstat -ano | findstr 27017

if ($mongo) {

    Write-Host "[OK] MongoDB ativo"

}
else {

    Write-Host "[ERRO] MongoDB nao encontrado"

}

# =========================
# GERAR RELATORIO
# =========================

Write-Host ""
Write-Host "5) GERANDO RELATORIO DE ARQUITETURA..."

$report = @()

$report += "CONSULT SLT - ARCHITECTURE REPORT"
$report += ""
$report += "SERVICOS DETECTADOS"
$report += "Frontend -> localhost:3000"
$report += "Backend -> localhost:8000"
$report += "API Gateway -> localhost:8001"
$report += "MongoDB -> localhost:27017"
$report += ""
$report += "ROTAS ENCONTRADAS"

foreach ($r in $routes) {

    $report += $r

}

$report += ""
$report += "RESULTADO DOS TESTES"

foreach ($r in $results) {

    $report += $r

}

$report += ""
$report += "POSSIVEIS CAUSAS DE ERRO"

$report += "401 -> rota exige autenticacao"
$report += "404 -> rota nao registrada"
$report += "500 -> erro interno backend"
$report += "NO RESPONSE -> servidor nao respondeu"

$report | Out-File $reportFile

Write-Host "OK -> $reportFile"

Write-Host ""
Write-Host "================================="
Write-Host "AUDITORIA SRE FINALIZADA"
Write-Host "================================="