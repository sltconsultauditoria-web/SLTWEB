Write-Host ""
Write-Host "====================================="
Write-Host "REPARANDO PATHS ERRADOS"
Write-Host "====================================="
Write-Host ""

$files = Get-ChildItem -Recurse -Include *.json,*.js,*.jsx,*.ts,*.tsx,*.html `
-File |
Where-Object {
$_.FullName -notmatch "node_modules" -and
$_.FullName -notmatch ".git" -and
$_.FullName -notmatch "build"
}

foreach ($file in $files) {

$content = Get-Content $file.FullName -Raw

$original = $content

# remove homepage errado
$content = $content -replace '"homepage":\s*"https://sltconsultauditoria-web.github.io/consultSLTweb-"\s*,?', ''

# remove PUBLIC_URL errado
$content = $content -replace 'PUBLIC_URL=/consultSLTweb-', ''

# remove basename errado
$content = $content -replace 'basename="/consultSLTweb-"', ''

# remove qualquer consultSLTweb-
$content = $content -replace 'consultSLTweb-', 'SLTWEB'

if ($content -ne $original){

Write-Host "Corrigido:" $file.FullName -ForegroundColor Green

Set-Content $file.FullName $content

}

}

Write-Host ""
Write-Host "====================================="
Write-Host "REPARO FINALIZADO"
Write-Host "====================================="
Write-Host ""