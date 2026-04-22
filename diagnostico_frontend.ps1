Write-Host "====================================="
Write-Host " DIAGNOSTICO FRONTEND (GITHUB PAGES)"
Write-Host "====================================="

# 1. Verificar build
Write-Host "`n[1] Verificando build..."
if (Test-Path "frontend/build/index.html") {
    Write-Host "OK: Build existe"
} else {
    Write-Host "ERRO: Build NÃO encontrado"
}

# 2. Verificar docs (GitHub Pages)
Write-Host "`n[2] Verificando /docs..."
if (Test-Path "docs/index.html") {
    Write-Host "OK: docs/index.html existe"
} else {
    Write-Host "ERRO: docs NÃO gerado"
}

# 3. Verificar JS
Write-Host "`n[3] Verificando JS..."
$js = Get-ChildItem -Path "docs/static/js" -ErrorAction SilentlyContinue
if ($js) {
    Write-Host "OK: JS encontrado"
} else {
    Write-Host "ERRO: JS não encontrado"
}

# 4. Verificar CSS
Write-Host "`n[4] Verificando CSS..."
$css = Get-ChildItem -Path "docs/static/css" -ErrorAction SilentlyContinue
if ($css) {
    Write-Host "OK: CSS encontrado"
} else {
    Write-Host "ERRO: CSS não encontrado"
}

# 5. Verificar homepage no package.json
Write-Host "`n[5] Verificando homepage..."
$pkg = Get-Content "frontend/package.json" -Raw
if ($pkg -match "homepage") {
    Write-Host "OK: homepage configurado"
} else {
    Write-Host "ERRO: homepage NÃO configurado"
}

# 6. Verificar caminhos quebrados
Write-Host "`n[6] Verificando caminhos no index.html..."
$index = Get-Content "docs/index.html" -Raw

if ($index -match 'src="/static') {
    Write-Host "ERRO: Caminho absoluto detectado (/static)"
    Write-Host "Isso causa tela branca no GitHub Pages"
} else {
    Write-Host "OK: caminhos relativos"
}

# 7. Verificar React root
Write-Host "`n[7] Verificando root div..."
if ($index -match 'id="root"') {
    Write-Host "OK: root encontrado"
} else {
    Write-Host "ERRO: root não encontrado"
}

# 8. Teste rápido de servidor local
Write-Host "`n[8] Teste local (opcional)..."
Write-Host "Execute manualmente:"
Write-Host "npx serve docs"

Write-Host "`n====================================="
Write-Host " FIM DO DIAGNOSTICO"
Write-Host "====================================="