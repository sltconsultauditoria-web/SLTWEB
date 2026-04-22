Write-Host ""
Write-Host "====================================="
Write-Host "PROCURANDO PATHS ERRADOS"
Write-Host "====================================="
Write-Host ""

$termos = @(
"consultSLTweb-",
"consultSLTweb",
"PUBLIC_URL",
"homepage",
"basename"
)

foreach ($termo in $termos) {

Write-Host ""
Write-Host "Procurando:" $termo -ForegroundColor Yellow

Get-ChildItem -Recurse -File |
Where-Object {
$_.FullName -notmatch "node_modules" -and
$_.FullName -notmatch ".git"
} |
Select-String -Pattern $termo |
ForEach-Object {

Write-Host ""
Write-Host "Arquivo:" $_.Path -ForegroundColor Cyan
Write-Host "Linha:" $_.LineNumber
Write-Host $_.Line

}

}

Write-Host ""
Write-Host "====================================="
Write-Host "BUSCA FINALIZADA"
Write-Host "====================================="
Write-Host ""