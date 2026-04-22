Clear-Host

Write-Host "====================================="
Write-Host "SRE ARCHITECTURE AUDIT - CONSULT SLT"
Write-Host "====================================="
Write-Host ""

$report = "SYSTEM_ARCHITECTURE.md"

if (Test-Path $report) {
    Remove-Item $report
}

"# SYSTEM ARCHITECTURE REPORT" | Out-File $report

Write-Host "Verificando portas..."

"## PORTAS ABERTAS" | Add-Content $report
"netstat -ano" | Add-Content $report
"netstat -ano | findstr LISTENING" | Add-Content $report
"netstat -ano | findstr LISTENING | Out-File portas.txt"
Get-Content portas.txt | Add-Content $report

Write-Host "Verificando frontend..."

"## FRONTEND" | Add-Content $report

if (Test-Path "package.json") {

    "package.json encontrado" | Add-Content $report

    $pkg = Get-Content package.json -Raw
    $pkg | Add-Content $report

}
else {

    "Frontend não encontrado" | Add-Content $report

}

Write-Host "Verificando backend..."

"## BACKEND" | Add-Content $report

$servers = Get-ChildItem -Recurse -Include server.js,app.js,index.js -ErrorAction SilentlyContinue

if ($servers) {

    "Servidor encontrado" | Add-Content $report

    foreach ($s in $servers) {

        $lines = Select-String -Path $s.FullName -Pattern "listen"

        foreach ($l in $lines) {

            $l.Line | Add-Content $report

        }

    }

}
else {

    "Backend não encontrado" | Add-Content $report

}

Write-Host "Mapeando rotas..."

"## ROTAS API" | Add-Content $report

$files = Get-ChildItem -Recurse -Include *.js

foreach ($file in $files) {

    $routes = Select-String -Path $file.FullName -Pattern "router."

    if ($routes) {

        $file.Name | Add-Content $report

        foreach ($r in $routes) {

            $r.Line | Add-Content $report

        }

    }

}

Write-Host "Verificando .env..."

"## VARIAVEIS DE AMBIENTE" | Add-Content $report

if (Test-Path ".env") {

    Get-Content ".env" | Add-Content $report

}
else {

    ".env não encontrado" | Add-Content $report

}

Write-Host "Testando MongoDB..."

"## MONGODB" | Add-Content $report

$mongo = Test-NetConnection 127.0.0.1 -Port 27017

if ($mongo.TcpTestSucceeded) {

    "MongoDB ativo" | Add-Content $report

}
else {

    "MongoDB não respondeu" | Add-Content $report

}

Write-Host "Testando APIs..."

"## TESTE API" | Add-Content $report

$urls = @("http://localhost:8000","http://localhost:3000")

foreach ($u in $urls) {

    try {

        Invoke-WebRequest $u -TimeoutSec 3 | Out-Null
        "$u OK" | Add-Content $report

    }
    catch {

        "$u FALHOU" | Add-Content $report

    }

}

Write-Host "Verificando GitHub Pages..."

"## GITHUB PAGES" | Add-Content $report

if (Test-Path "docs/index.html") {

    "Build encontrado em docs" | Add-Content $report

}
else {

    "Build docs não encontrado" | Add-Content $report

}

Write-Host ""
Write-Host "Relatorio gerado:"
Write-Host $report
Write-Host ""
Write-Host "AUDITORIA FINALIZADA"