Write-Host ""
Write-Host "====================================="
Write-Host "SLTWEB FRONTEND PROFESSIONAL SETUP"
Write-Host "====================================="
Write-Host ""

Write-Host "1 - Limpando ambiente..."

Remove-Item -Recurse -Force build -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force docs -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force node_modules -ErrorAction SilentlyContinue

Remove-Item package-lock.json -ErrorAction SilentlyContinue

Write-Host "OK"

Write-Host ""
Write-Host "2 - Instalando dependencias..."

npm install

if ($LASTEXITCODE -ne 0){

Write-Host "ERRO npm install" -ForegroundColor Red
exit

}

Write-Host "OK"

Write-Host ""
Write-Host "3 - Instalando gh-pages..."

npm install gh-pages --save-dev

Write-Host "OK"

Write-Host ""
Write-Host "4 - Executando build..."

npm run build

if ($LASTEXITCODE -ne 0){

Write-Host "BUILD FALHOU" -ForegroundColor Red
exit

}

Write-Host "OK"

Write-Host ""
Write-Host "5 - Deploy GitHub Pages..."

npm run deploy

if ($LASTEXITCODE -ne 0){

Write-Host "DEPLOY FALHOU" -ForegroundColor Red
exit

}

Write-Host ""
Write-Host "====================================="
Write-Host "DEPLOY FINALIZADO"
Write-Host "====================================="
Write-Host ""

Write-Host "URL:"
Write-Host "https://sltconsultauditoria-web.github.io/SLTWEB/"

Write-Host ""