Write-Host "====================================="
Write-Host "ANALISE DE TECNOLOGIAS DO PROJETO"
Write-Host "====================================="
Write-Host ""

$root = Get-Location

# ----------------------------
# Backend - Python
# ----------------------------
Write-Host "BACKEND (Python)" -ForegroundColor Cyan
Write-Host "------------------"

if (Test-Path ".\backend") {
    Write-Host "Pasta backend encontrada."

    # Verificar requirements.txt
    if (Test-Path ".\requirements.txt") {
        Write-Host ""
        Write-Host "Pacotes encontrados em requirements.txt:"
        Get-Content ".\requirements.txt"
    }

    # Procurar tecnologias comuns
    $pythonFiles = Get-ChildItem ".\backend" -Recurse -Filter "*.py"

    $techs = @()

    foreach ($file in $pythonFiles) {
        $content = Get-Content $file.FullName -Raw

        if ($content -match "fastapi") { $techs += "FastAPI" }
        if ($content -match "motor") { $techs += "Motor (Mongo Async)" }
        if ($content -match "pymongo") { $techs += "PyMongo" }
        if ($content -match "jwt") { $techs += "JWT Authentication" }
        if ($content -match "passlib") { $techs += "Password Hashing (Passlib)" }
        if ($content -match "uvicorn") { $techs += "Uvicorn ASGI Server" }
        if ($content -match "cors") { $techs += "CORS Middleware" }
    }

    $techs = $techs | Sort-Object -Unique

    Write-Host ""
    Write-Host "Tecnologias detectadas no backend:"
    $techs
}
else {
    Write-Host "Pasta backend nao encontrada."
}

Write-Host ""
Write-Host ""

# ----------------------------
# Frontend - Node / React
# ----------------------------
Write-Host "FRONTEND (Node/React)" -ForegroundColor Yellow
Write-Host "-----------------------"

if (Test-Path ".\frontend\package.json") {

    $packageJson = Get-Content ".\frontend\package.json" -Raw | ConvertFrom-Json

    Write-Host ""
    Write-Host "Dependencias:"
    $packageJson.dependencies.Keys

    Write-Host ""
    Write-Host "DevDependencias:"
    $packageJson.devDependencies.Keys

}
else {
    Write-Host "package.json nao encontrado."
}

Write-Host ""
Write-Host "====================================="
Write-Host "ANALISE FINALIZADA"
Write-Host "====================================="
