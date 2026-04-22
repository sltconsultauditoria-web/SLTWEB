Clear-Host

Write-Host "AUDITORIA FRONTEND" -ForegroundColor Cyan
Write-Host ""

Write-Host "CONFIGS:" -ForegroundColor Yellow
Get-ChildItem *.config.js, jsconfig.json, components.json

Write-Host ""
Write-Host "API DUPLICADA:" -ForegroundColor Yellow
Get-ChildItem -Recurse -Filter api.js

Write-Host ""
Write-Host "TAILWIND IMPORTS:" -ForegroundColor Yellow
Get-Content .\src\index.css | Select-String "@tailwind","@apply"

Write-Host ""
Write-Host "ALIASES @/ :" -ForegroundColor Yellow
Get-ChildItem .\src -Recurse -Include *.js,*.jsx |
Select-String "@/" | Select-Object -First 20

Write-Host ""
Write-Host "IMPORTS api.js :" -ForegroundColor Yellow
Get-ChildItem .\src -Recurse -Include *.js,*.jsx |
Select-String "api.js","services/api"

Write-Host ""
Write-Host "FIM."