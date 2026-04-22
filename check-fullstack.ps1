Write-Host ""
Write-Host "==========================================="
Write-Host "DIAGNOSTICO FULLSTACK - CONSULT SLT"
Write-Host "Frontend + API + MongoDB"
Write-Host "==========================================="
Write-Host ""

$frontend = "frontend"
$backend = "backend"

# -----------------------------
# 1 NODE
# -----------------------------

Write-Host "1️⃣ Verificando Node"

node -v
npm -v

# -----------------------------
# 2 FRONTEND
# -----------------------------

Write-Host ""
Write-Host "2️⃣ Verificando Frontend"

if(Test-Path "$frontend/package.json"){
    Write-Host "Frontend encontrado"
}else{
    Write-Host "ERRO: frontend nao encontrado"
}

if(Test-Path "$frontend/build"){
    Write-Host "Build frontend existe"
}else{
    Write-Host "Build frontend nao existe"
}

if(Test-Path "$frontend/docs"){
    Write-Host "Docs para GitHub Pages existe"
}else{
    Write-Host "Docs nao existe"
}

# -----------------------------
# 3 GITHUB PAGES
# -----------------------------

Write-Host ""
Write-Host "3️⃣ Verificando GitHub Pages"

$pkg = Get-Content "$frontend/package.json" -Raw

if($pkg -match "homepage"){
    Write-Host "homepage configurado"
}else{
    Write-Host "homepage NAO configurado"
}

# -----------------------------
# 4 BACKEND
# -----------------------------

Write-Host ""
Write-Host "4️⃣ Verificando Backend"

if(Test-Path "$backend"){
    Write-Host "Backend encontrado"
}else{
    Write-Host "Backend NAO encontrado"
}

if(Test-Path "$backend/package.json"){
    Write-Host "Backend Node detectado"
}

# -----------------------------
# 5 .ENV
# -----------------------------

Write-Host ""
Write-Host "5️⃣ Verificando ENV"

if(Test-Path "$backend/.env"){
    Write-Host ".env encontrado"
}else{
    Write-Host "ERRO: .env nao encontrado"
}

# -----------------------------
# 6 MONGODB
# -----------------------------

Write-Host ""
Write-Host "6️⃣ Verificando MongoDB"

$mongoTest = Test-NetConnection -ComputerName localhost -Port 27017 -WarningAction SilentlyContinue

if($mongoTest.TcpTestSucceeded){
    Write-Host "MongoDB rodando"
}else{
    Write-Host "MongoDB NAO acessivel"
}

# -----------------------------
# 7 API GATEWAY
# -----------------------------

Write-Host ""
Write-Host "7️⃣ Testando API Gateway"

try{
    $res = Invoke-WebRequest "http://localhost:3000/api/health" -UseBasicParsing
    Write-Host "API Gateway respondeu"
}catch{
    Write-Host "API Gateway NAO respondeu"
}

# -----------------------------
# 8 BACKEND API
# -----------------------------

Write-Host ""
Write-Host "8️⃣ Testando Backend"

try{
    $res = Invoke-WebRequest "http://localhost:5000/api/health" -UseBasicParsing
    Write-Host "Backend respondeu"
}catch{
    Write-Host "Backend NAO respondeu"
}

# -----------------------------
# 9 ROTAS
# -----------------------------

Write-Host ""
Write-Host "9️⃣ Testando rotas principais"

$rotas = @(
"/api/login",
"/api/consulta",
"/api/auditoria"
)

foreach($r in $rotas){

    try{
        Invoke-WebRequest "http://localhost:5000$r" -UseBasicParsing
        Write-Host "$r OK"
    }catch{
        Write-Host "$r FALHOU"
    }

}

# -----------------------------
# 10 RELATORIO
# -----------------------------

Write-Host ""
Write-Host "==========================================="
Write-Host "DIAGNOSTICO FINALIZADO"
Write-Host "==========================================="