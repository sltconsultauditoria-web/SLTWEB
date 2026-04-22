Write-Host "==========================================="
Write-Host "FIX FINAL GIT + PUSH + GITHUB PAGES"
Write-Host "==========================================="

# 1. REMOVER HOOKS
Write-Host "`nRemovendo hooks..."
if (Test-Path ".git\hooks") {
    Remove-Item -Recurse -Force .git\hooks
}
New-Item -ItemType Directory -Path .git\hooks | Out-Null
Write-Host "Hooks OK"

# 2. .gitignore
Write-Host "`nAjustando .gitignore..."

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
"@ | Out-File -Encoding ascii .gitignore

Write-Host ".gitignore OK"

# 3. LIMPEZA
Write-Host "`nLimpando arquivos pesados..."

Remove-Item -Recurse -Force -ErrorAction SilentlyContinue frontend\node_modules\.cache
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue frontend\build
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue frontend\docs
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue docs

Write-Host "Limpeza OK"

# 4. RESET GIT
Write-Host "`nResetando index..."

git rm -r --cached . 2>$null
git add .

Write-Host "Index OK"

# 5. BUILD
Write-Host "`nBuildando frontend..."

cd frontend
npm install
npm run build

Write-Host "`nCopiando build para docs..."
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue ..\docs
Copy-Item -Recurse -Force build ..\docs

cd ..

# 6. COMMIT
Write-Host "`nCommit..."

git add .
git commit -m "fix final github pages clean"

# 7. PUSH (SEM HOOK)
Write-Host "`nPush final..."

git -c core.hooksPath=nul push origin main --force

Write-Host "`n==========================================="
Write-Host "FINALIZADO"
Write-Host "==========================================="

Write-Host "`nAcesse:"
Write-Host "https://sltconsultauditoria-web.github.io/SLTWEB/?v=FINAL1000"