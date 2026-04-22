Write-Host ""
Write-Host "============================================"
Write-Host "ENGENHARIA REVERSA DO SISTEMA CONSULT SLT"
Write-Host "============================================"
Write-Host ""

$root = Get-Location
$frontend = "$root\frontend"
$backend = "$root\backend"

# ----------------------------------
# 1 PORTAS ABERTAS
# ----------------------------------

Write-Host ""
Write-Host "1️⃣ Mapeando portas abertas..."

netstat -ano | findstr LISTENING

# ----------------------------------
# 2 FRONTEND
# ----------------------------------

Write-Host ""
Write-Host "2️⃣ Verificando frontend..."

if(Test-Path "$frontend"){

Write-Host "Frontend encontrado"

if(Test-Path "$frontend\package.json"){

Write-Host "package.json encontrado"

$pkg = Get-Content "$frontend\package.json" -Raw

if($pkg -match "react"){
Write-Host "Aplicacao React detectada"
}

if($pkg -match "homepage"){
Write-Host "Configurado para GitHub Pages"
}

}

if(Test-Path "$frontend\build"){
Write-Host "Build encontrado"
}

if(Test-Path "$frontend\docs"){
Write-Host "Docs para deploy encontrados"
}

}else{

Write-Host "Frontend nao encontrado"

}

# ----------------------------------
# 3 BACKEND
# ----------------------------------

Write-Host ""
Write-Host "3️⃣ Verificando backend..."

if(Test-Path "$backend"){

Write-Host "Backend encontrado"

Get-ChildItem $backend -Filter "*.js" -Recurse |
Select-String "app.listen" |
ForEach-Object {

Write-Host "Servidor encontrado em:"
Write-Host $_.Path
Write-Host $_.Line

}

}else{

Write-Host "Backend nao encontrado"

}

# ----------------------------------
# 4 VARIAVEIS ENV
# ----------------------------------

Write-Host ""
Write-Host "4️⃣ Verificando variaveis ENV..."

if(Test-Path "$backend\.env"){

Get-Content "$backend\.env"

}else{

Write-Host ".env nao encontrado"

}

# ----------------------------------
# 5 ROTAS API
# ----------------------------------

Write-Host ""
Write-Host "5️⃣ Descobrindo rotas da API..."

Get-ChildItem $backend -Filter "*.js" -Recurse |
Select-String "router." |
ForEach-Object {

Write-Host $_.Line

}

# ----------------------------------
# 6 MONGODB
# ----------------------------------

Write-Host ""
Write-Host "6️⃣ Verificando MongoDB..."

$mongo = Test-NetConnection localhost -Port 27017 -WarningAction SilentlyContinue

if($mongo.TcpTestSucceeded){

Write-Host "MongoDB ativo"

}else{

Write-Host "MongoDB nao responde"

}

# ----------------------------------
# 7 TESTE API
# ----------------------------------

Write-Host ""
Write-Host "7️⃣ Testando endpoints comuns..."

$portas = @(3000,3001,4000,5000,8000,8001)

foreach($p in $portas){

try{

$res = Invoke-WebRequest "http://localhost:$p/api" -UseBasicParsing -TimeoutSec 2

Write-Host "API encontrada na porta $p"

}catch{}

}

# ----------------------------------
# 8 DEPENDENCIAS
# ----------------------------------

Write-Host ""
Write-Host "8️⃣ Dependencias backend..."

if(Test-Path "$backend\package.json"){

npm --prefix $backend list --depth=0

}

Write-Host ""
Write-Host "============================================"
Write-Host "ANALISE FINAL CONCLUIDA"
Write-Host "============================================"