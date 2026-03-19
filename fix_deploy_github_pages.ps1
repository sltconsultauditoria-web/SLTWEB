Write-Host "====================================="
Write-Host " FIX DEPLOY GITHUB PAGES (REACT)"
Write-Host "====================================="

# =========================
# CONFIG
# =========================
$PROJECT_NAME = "SLTWEB"
$FRONTEND_PATH = "frontend"

# =========================
# STEP 1 - CLEAN
# =========================
Write-Host "`n[1] Limpando builds antigos..."

Remove-Item -Recurse -Force "$FRONTEND_PATH/build" -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force "$FRONTEND_PATH/docs" -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force "docs" -ErrorAction SilentlyContinue

# =========================
# STEP 2 - SET PUBLIC URL
# =========================
Write-Host "`n[2] Definindo PUBLIC_URL..."


# =========================
# STEP 3 - BUILD
# =========================
Write-Host "`n[3] Gerando build..."

cd $FRONTEND_PATH

npm install
npm run build

if (!(Test-Path "build/index.html")) {
    Write-Host "❌ ERRO: build falhou"
    exit
}

Write-Host "✅ Build gerado"

# =========================
# STEP 4 - COPY TO DOCS
# =========================
Write-Host "`n[4] Copiando para /docs..."

cd ..

Copy-Item -Recurse -Force "$FRONTEND_PATH/build" "docs"

if (!(Test-Path "docs/index.html")) {
    Write-Host "❌ ERRO: docs não criado"
    exit
}

Write-Host "✅ docs criado"

# =========================
# STEP 5 - VALIDATE PATHS
# =========================
Write-Host "`n[5] Validando caminhos..."

$content = Get-Content "docs/index.html" -Raw

if ($content -match "/static/") {
    Write-Host "❌ ERRO: caminhos ainda estão ABSOLUTOS (/static)"
    Write-Host "➡️ PUBLIC_URL não aplicado corretamente"
    exit
}

if ($content -match "/$PROJECT_NAME/static/") {
    Write-Host "✅ Caminhos corrigidos (/SLTWEB/static)"
} else {
    Write-Host "⚠️ Aviso: não encontrou padrão esperado"
}

# =========================
# STEP 6 - GIT
# =========================
Write-Host "`n[6] Commit + Push..."

git add .
git commit -m "fix: deploy github pages corrigido" 2>$null

git push origin main --force

Write-Host "`n====================================="
Write-Host " DEPLOY FINALIZADO"
Write-Host "====================================="
Write-Host "Acesse:"
Write-Host "https://sltconsultauditoria-web.github.io/$PROJECT_NAME/"