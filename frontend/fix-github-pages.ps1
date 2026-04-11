Write-Host ""
Write-Host "====================================="
Write-Host "SLTWEB GITHUB PAGES FIX"
Write-Host "====================================="
Write-Host ""

Write-Host "1 - Removendo docs antigo..."

Remove-Item -Recurse -Force docs -ErrorAction SilentlyContinue

git rm -r docs 2>$null

git commit -m "remove old docs deploy" 2>$null

Write-Host "OK"

Write-Host ""
Write-Host "2 - Limpando build..."

Remove-Item -Recurse -Force build -ErrorAction SilentlyContinue

Write-Host "OK"

Write-Host ""
Write-Host "3 - Reinstalando dependencias..."

Remove-Item -Recurse -Force node_modules -ErrorAction SilentlyContinue

Remove-Item package-lock.json -ErrorAction SilentlyContinue

npm install

Write-Host "OK"

Write-Host ""
Write-Host "4 - Build limpo..."

npm run build

Write-Host "OK"

Write-Host ""
Write-Host "5 - Deploy gh-pages..."

npm run deploy

Write-Host "OK"

Write-Host ""
Write-Host "6 - Push final..."

git push

Write-Host "OK"

Write-Host ""
Write-Host "====================================="
Write-Host "DEPLOY CORRIGIDO"
Write-Host "====================================="
Write-Host ""

Write-Host "Agora ajuste no GitHub:"
Write-Host ""
Write-Host "Settings → Pages"
Write-Host "Branch → gh-pages"
Write-Host "Folder → /(root)"
Write-Host ""
Write-Host "URL:"
Write-Host "https://sltconsultauditoria-web.github.io/SLTWEB/"
Write-Host ""
