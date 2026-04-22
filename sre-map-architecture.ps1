Write-Host ""
Write-Host "CONSULT SLT - SRE ARCHITECTURE MAPPER"
Write-Host "====================================="

$root = Get-Location
$treeFile = "estrutura-app.txt"

Write-Host ""
Write-Host "GERANDO TREE DA APLICACAO..."

cmd /c tree /F /A > $treeFile

Write-Host "Tree salvo em $treeFile"

Write-Host ""
Write-Host "PROCURANDO ROTAS DA API..."

$routes = @()

$files = Get-ChildItem -Recurse -Include *.js,*.ts,*.py

foreach ($file in $files) {

    $content = Get-Content $file.FullName

    foreach ($line in $content) {

        if ($line -match "/api/") {

            $route = $line.Trim()

            if ($routes -notcontains $route) {

                $routes += $route

            }

        }

    }

}

Write-Host ""
Write-Host "ROTAS ENCONTRADAS"

foreach ($r in $routes) {

    Write-Host $r

}

Write-Host ""
Write-Host "TESTANDO ROTAS..."

foreach ($route in $routes) {

    if ($route -match "/api/[a-zA-Z0-9/_-]+") {

        $endpoint = $matches[0]

        $url = "http://localhost:8000$endpoint"

        try {

            $response = Invoke-WebRequest $url -UseBasicParsing -TimeoutSec 3

            Write-Host "[OK] $endpoint -> $($response.StatusCode)"

        }
        catch {

            if ($_.Exception.Response) {

                $status = $_.Exception.Response.StatusCode.value__

                Write-Host "[FAIL] $endpoint -> $status"

            }
            else {

                Write-Host "[FAIL] $endpoint -> sem resposta"

            }

        }

    }

}

Write-Host ""
Write-Host "ANALISE DE PROBLEMAS..."

Write-Host ""
Write-Host "Possiveis causas para falha:"
Write-Host "1. Endpoint exige autenticacao JWT"
Write-Host "2. Metodo HTTP incorreto (GET vs POST)"
Write-Host "3. Middleware bloqueando"
Write-Host "4. Erro interno do backend"
Write-Host "5. Rota nao registrada no router"

Write-Host ""
Write-Host "MAPEAMENTO FINALIZADO"