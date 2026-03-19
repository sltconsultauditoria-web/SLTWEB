Write-Host ""
Write-Host "🚀 SRE ARCHITECTURE CHECK"
Write-Host "=========================="

# MongoDB
Write-Host ""
Write-Host "🔎 MongoDB"

try {
    mongo --eval "db.stats()" | Out-Null
    Write-Host "✅ MongoDB OK"
}
catch {
    Write-Host "❌ MongoDB não respondeu"
}

# Backend
Write-Host ""
Write-Host "🔎 Backend API"

try {
    $response = Invoke-WebRequest http://localhost:8000/docs -UseBasicParsing
    Write-Host "✅ Backend FastAPI OK"
}
catch {
    Write-Host "❌ Backend não respondeu"
}

# Frontend
Write-Host ""
Write-Host "🔎 Frontend"

try {
    $response = Invoke-WebRequest http://localhost:3000 -UseBasicParsing
    Write-Host "✅ Frontend OK"
}
catch {
    Write-Host "❌ Frontend não respondeu"
}

# API Gateway
Write-Host ""
Write-Host "🔎 API Gateway"

try {
    $response = Invoke-WebRequest http://localhost:8080 -UseBasicParsing
    Write-Host "✅ Gateway OK"
}
catch {
    Write-Host "⚠️ Gateway não encontrado"
}

Write-Host ""
Write-Host "🏁 CHECK FINALIZADO"