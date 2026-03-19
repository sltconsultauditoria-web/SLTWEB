Write-Host "==============================="
Write-Host "DIAGNOSTICO GITHUB PAGES"
Write-Host "==============================="

# verificar estrutura
Write-Host "`nVerificando estrutura do projeto..."

if (Test-Path "frontend/package.json") {
    Write-Host "Frontend detectado"
} else {
    Write-Host "Frontend NAO encontrado"
}

# verificar homepage
Write-Host "`nVerificando homepage no package.json"

$pkg = Get-Content "frontend/package.json" -Raw

if ($pkg -match "homepage") {
    Write-Host "homepage configurado"
} else {
    Write-Host "ERRO: homepage nao configurado"
}

# verificar build
Write-Host "`nVerificando pasta build..."

if (Test-Path "frontend/build/index.html") {
    Write-Host "Build OK"
} else {
    Write-Host "Build nao encontrado"
}

# verificar docs
Write-Host "`nVerificando pasta docs..."

if (Test-Path "frontend/docs/index.html") {
    Write-Host "Docs OK"
} else {
    Write-Host "Docs nao encontrado"
}

Write-Host "`nDiagnostico finalizado."