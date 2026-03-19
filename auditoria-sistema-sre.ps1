Write-Host ""
Write-Host "======================================="
Write-Host "AUDITORIA COMPLETA DO SISTEMA"
Write-Host "======================================="

$root = Get-Location
$backend = "$root\backend"
$frontend = "$root\frontend"

$report = "$root\system-architecture.md"

"# SYSTEM ARCHITECTURE REPORT" | Out-File $report

# PORTAS

Add-Content $report "`n## Portas abertas"

netstat -ano | findstr LISTENING | Out-File -Append $report

# FRONTEND

Add-Content $report "`n## Frontend"

if(Test-Path "$frontend\package.json"){

$pkg = Get-Content "$frontend\package.json" -Raw

if($pkg -match "react"){

Add-Content $report "React detectado"

}

}

# BACKEND

Add-Content $report "`n## Backend"

Get-ChildItem $backend -Filter "*.js" -Recurse |
Select-String "app.listen" |
ForEach-Object {

Add-Content $report $_.Line

}

# ROTAS API

Add-Content $report "`n## Rotas API"

Get-ChildItem $backend -Filter "*.js" -Recurse |
Select-String "router." |
ForEach-Object {

Add-Content $report $_.Line

}

# DEPENDENCIAS

Add-Content $report "`n## Dependencias"

npm --prefix $backend list --depth=0 | Out-File -Append $report

# ENV

Add-Content $report "`n## Variaveis de ambiente"

Get-Content "$backend\.env" | Out-File -Append $report

# MONGODB

Add-Content $report "`n## MongoDB"

$mongo = Test-NetConnection localhost -Port 27017

if($mongo.TcpTestSucceeded){

Add-Content $report "MongoDB ativo"

}

Write-Host ""
Write-Host "Relatorio gerado em:"
Write-Host $report