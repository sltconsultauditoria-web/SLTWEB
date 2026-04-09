Write-Host ""
Write-Host "====================================="
Write-Host "CORRIGINDO PACKAGE.JSON"
Write-Host "====================================="
Write-Host ""

$file="package.json"

$json = Get-Content $file -Raw

Write-Host "Corrigindo scripts..."

$json = $json -replace '"postbuild".*', ''
$json = $json -replace 'git add frontend/docs -f', 'gh-pages -d build'
$json = $json -replace '"deploy".*', '"deploy": "gh-pages -d build",'
$json = $json -replace '"build".*', '"build": "craco build",'

if($json -notmatch "predeploy"){

$json = $json -replace '"build": "craco build",',
'"build": "craco build",
"predeploy": "npm run build",'

}

Set-Content $file $json

Write-Host "OK"

Write-Host ""
Write-Host "Removendo docs antigo..."

Remove-Item -Recurse -Force docs -ErrorAction SilentlyContinue

Write-Host "OK"

Write-Host ""
Write-Host "Instalando gh-pages..."

npm install gh-pages --save-dev

Write-Host ""
Write-Host "====================================="
Write-Host "PACKAGE.JSON CORRIGIDO"
Write-Host "====================================="
Write-Host ""

Write-Host "Agora execute:"
Write-Host "npm run deploy"
Write-Host ""