Write-Host ""
Write-Host "CONSULT SLT - SAFE SRE ANALYZER"
Write-Host "--------------------------------"

$root = Get-Location
$backend = "$root\backend"
$report = "$root\sre-report.txt"
$routesFile = "$root\sre-routes.txt"

Remove-Item $report -ErrorAction SilentlyContinue
Remove-Item $routesFile -ErrorAction SilentlyContinue

Write-Host "1) Gerando TREE da aplicação..."

tree /F /A > "$root\sre-tree.txt"

Write-Host "TREE salvo em sre-tree.txt"

Write-Host ""
Write-Host "2) Escaneando rotas FastAPI..."

Get-ChildItem -Recurse -Include *.py | ForEach-Object {

    Select-String -Path $_.FullName -Pattern "@router.get","@router.post","@router.put","@router.delete" |
    ForEach-Object {

        $line = $_.Line.Trim()

        if ($line -match '\("(.*?)"\)') {

            $route = $matches[1]

            if ($route -notmatch "http") {

                Add-Content $routesFile $route

            }
        }

    }

}

Write-Host "Rotas detectadas em $routesFile"

Write-Host ""
Write-Host "3) Normalizando rotas..."

$routes = Get-Content $routesFile | Sort-Object | Get-Unique

$normalized = @()

foreach ($r in $routes) {

    if ($r.StartsWith("/api") -eq $false) {

        $normalized += "/api$r"

    } else {

        $normalized += $r

    }

}

$normalized | Set-Content "$root\sre-routes-normalized.txt"

Write-Host "Rotas normalizadas"

Write-Host ""
Write-Host "4) Testando endpoints..."

foreach ($route in $normalized) {

    $url = "http://localhost:8000$route"

    try {

        $res = Invoke-WebRequest $url -TimeoutSec 3 -UseBasicParsing

        "$route -> $($res.StatusCode)" | Tee-Object -FilePath $report -Append

    } catch {

        "$route -> ERROR" | Tee-Object -FilePath $report -Append

    }

}

Write-Host ""
Write-Host "5) Criando alias seguro (opcional)"

$aliasFile = "$backend\route_aliases_autogen.py"

@"
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

def ok(name):
    async def endpoint():
        return {"status":"ok","alias":name}
    return endpoint

"@ | Set-Content $aliasFile

foreach ($route in $normalized) {

    $safe = $route.Replace("/","_").Replace("-","_")

    @"

router.add_api_route(
    "$route",
    ok("$route"),
    methods=["GET"]
)

"@ | Add-Content $aliasFile

}

Write-Host "Alias gerados em route_aliases_autogen.py"

Write-Host ""
Write-Host "6) Relatorio final"

Get-Content $report

Write-Host ""
Write-Host "Arquivos gerados:"
Write-Host "sre-tree.txt"
Write-Host "sre-routes.txt"
Write-Host "sre-routes-normalized.txt"
Write-Host "sre-report.txt"
Write-Host "backend\route_aliases_autogen.py"

Write-Host ""
Write-Host "Script concluido sem modificar codigo existente."