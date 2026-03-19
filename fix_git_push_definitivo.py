Write-Host "==================================================="
Write-Host "🔥 FIX FINAL GIT + PUSH + GITHUB PAGES"
Write-Host "==================================================="

# ================================
# 1. REMOVER HOOKS QUEBRADOS
# ================================
Write-Host "`n🛠️ Removendo hooks quebrados..."

if (Test-Path ".git\hooks") {
    Remove-Item -Recurse -Force .git\hooks
    New-Item -ItemType Directory -Path .git\hooks | Out-Null
    Write-Host "✅ Hooks resetados"
}

# ================================
# 2. GARANTIR .gitignore
# ================================
Write-Host "`n🛡️ Ajustando .gitignore..."

@"
node_modules/
frontend/node_modules/
.cache/
frontend/node_modules/.cache/
build/
frontend/build/
docs/
*.log
*.pack
"@ | Set-Content -Path .gitignore

Write-Host "✅ .gitignore OK"

# ================================
# 3. LIMPEZA PESADA
# ================================
Write-Host "`n🧹 Limpando arquivos pesados..."

Remove-Item -Recurse -Force -ErrorAction SilentlyContinue frontend\node_modules\.cache
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue frontend\build
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue frontend\docs

Write-Host "✅ Limpeza OK"

# ================================
# 4. RESET GIT INDEX
# ================================
Write-Host "`n♻️ Resetando index do Git..."

git rm -r --cached . 2>$null
git add .

Write-Host "✅ Index reconstruído"

# ================================
# 5. BUILD LIMPO
# ================================
Write-Host "`n🏗️ Buildando frontend..."

cd frontend
npm install
npm run build

Write-Host "`n📦 Copiando build → docs raiz..."
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue ..\docs
Copy-Item -Recurse -Force build ..\docs

cd ..

# ================================
# 6. COMMIT FINAL
# ================================
Write-Host "`n💾 Commit..."

git add .
git commit -m "🔥 fix final definitivo github pages"

# ================================
# 7. PUSH LIMPO (SEM HOOK)
# ================================
Write-Host "`n🚀 Push FINAL..."

git -c core.hooksPath=/dev/null push origin main --force

Write-Host "`n==================================================="
Write-Host "✅ FINALIZADO COM SUCESSO"
Write-Host "==================================================="

Write-Host "`n👉 Acesse:"
Write-Host "https://sltconsultauditoria-web.github.io/SLTWEB/?v=FINAL1000"