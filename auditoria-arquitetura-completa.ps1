Write-Host ""
Write-Host "======================================"
Write-Host "AUDITORIA COMPLETA DE ARQUITETURA"
Write-Host "======================================"

$root = Get-Location
$backend = "$root\backend"
$frontend = "$root\frontend"

$arch = "$root\architecture-diagram.md"
$api = "$root\api-documentation.md"
$db = "$root\database-map.md"

# -------------------------------
# ARQUITETURA
# -------------------------------

"# SYSTEM ARCHITECTURE" | Out-File $arch

Add-Content $arch "Frontend → Backend → MongoDB"

Add-Content $arch "`n## Portas detectadas"

netstat -ano | findstr LISTENING | Out-File -Append $arch

# -------------------------------
# FRONTEND
# -------------------------------

Add-Content $arch "`n## Frontend"

if(Test-Path "$frontend\package.json"){

$pkg = Get-Content "$frontend\package.json" -Raw

if($pkg -match "react"){
Add-Content $arch "React detectado"
}

if($pkg -match "tailwind"){
Add-Content $arch "Tailwind detectado"
}

}

# -------------------------------
# BACKEND
# -------------------------------

Add-Content $arch "`n## Backend"

Get-ChildItem $backend -Filter "*.js" -Recurse |
Select-String "app.listen" |
ForEach-Object {

Add-Content $arch $_.Line

}

# -------------------------------
# API DOCUMENTATION
# -------------------------------

"# API DOCUMENTATION" | Out-File $api

Get-ChildItem $backend -Filter "*.js" -Recurse |
Select-String "router." |
ForEach-Object {

Add-Content $api $_.Line

}

# -------------------------------
# DATABASE
# -------------------------------

"# DATABASE MAP" | Out-File $db

Add-Content $db "MongoDB connection test"

$mongo = Test-NetConnection localhost -Port 27017 -WarningAction SilentlyContinue

if($mongo.TcpTestSucceeded){

Add-Content $db "MongoDB ativo"

}

# -------------------------------
# DETECTAR COLLECTIONS
# -------------------------------

Write-Host ""
Write-Host "Tentando detectar collections..."

$collectionsEndpoint = "http://localhost:8000/db/collections"

try {

$res = Invoke-WebRequest $collectionsEndpoint -UseBasicParsing -TimeoutSec 3

$res.Content | Out-File -Append $db

}
catch {

Add-Content $db "Endpoint /db/collections nao respondeu"

}

# -------------------------------
# INTEGRACOES EXTERNAS
# -------------------------------

Add-Content $arch "`n## Integracoes externas"

if(Test-Path "$backend\.env"){

$env = Get-Content "$backend\.env"

if($env -match "SHAREPOINT"){
Add-Content $arch "SharePoint detectado"
}

if($env -match "TENANT"){
Add-Content $arch "Azure Entra ID detectado"
}

}

Write-Host ""
Write-Host "======================================"
Write-Host "RELATORIOS GERADOS"
Write-Host "======================================"

Write-Host "architecture-diagram.md"
Write-Host "api-documentation.md"
Write-Host "database-map.md"