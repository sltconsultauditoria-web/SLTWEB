# ==========================================================
# AUDITORIA FRONTEND REACT / CRACO / TAILWIND / DUPLICIDADES
# Rode dentro da pasta: frontend
# ==========================================================

Clear-Host
Write-Host ""
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host " AUDITORIA COMPLETA FRONTEND SLTWEB "
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

# ----------------------------------------------------------
# 1. Arquivos críticos
# ----------------------------------------------------------
Write-Host "1) Verificando arquivos principais..." -ForegroundColor Yellow

$arquivos = @(
".env",
"package.json",
"craco.config.js",
"tailwind.config.js",
"postcss.config.js",
"src\api.js",
"src\services\api.js",
"src\App.js",
"src\index.js",
"src\index.css"
)

foreach ($a in $arquivos) {
    if (Test-Path $a) {
        Write-Host " OK  $a" -ForegroundColor Green
    } else {
        Write-Host " FALTA $a" -ForegroundColor Red
    }
}

Write-Host ""

# ----------------------------------------------------------
# 2. Verifica duplicidade api.js
# ----------------------------------------------------------
Write-Host "2) Procurando api.js duplicados..." -ForegroundColor Yellow

Get-ChildItem . -Recurse -Filter api.js | ForEach-Object {
    Write-Host " API ENCONTRADA: $($_.FullName)" -ForegroundColor Cyan
}

Write-Host ""

# ----------------------------------------------------------
# 3. Imports errados / duplicados
# ----------------------------------------------------------
Write-Host "3) Procurando imports de api.js..." -ForegroundColor Yellow

Get-ChildItem .\src -Recurse -Include *.js,*.jsx |
Select-String -Pattern "api.js","services/api","from '../api'","from '../../api'" |
ForEach-Object {
    Write-Host "$($_.Path):$($_.LineNumber)" -ForegroundColor Magenta
    Write-Host "   $($_.Line.Trim())"
}

Write-Host ""

# ----------------------------------------------------------
# 4. Alias @/
# ----------------------------------------------------------
Write-Host "4) Procurando uso de alias '@/'" -ForegroundColor Yellow

Get-ChildItem .\src -Recurse -Include *.js,*.jsx |
Select-String -Pattern '@/'
| ForEach-Object {
    Write-Host "$($_.Path):$($_.LineNumber)" -ForegroundColor Blue
    Write-Host "   $($_.Line.Trim())"
}

Write-Host ""

# ----------------------------------------------------------
# 5. Tailwind directives
# ----------------------------------------------------------
Write-Host "5) Verificando Tailwind no index.css..." -ForegroundColor Yellow

if (Test-Path ".\src\index.css") {
    Get-Content ".\src\index.css" |
    Select-String "@tailwind","@apply" |
    ForEach-Object {
        Write-Host "   $($_.Line.Trim())" -ForegroundColor Green
    }
}

Write-Host ""

# ----------------------------------------------------------
# 6. Dependências suspeitas
# ----------------------------------------------------------
Write-Host "6) Verificando package.json..." -ForegroundColor Yellow

if (Test-Path ".\package.json") {

    $pkg = Get-Content package.json -Raw

    if ($pkg -match "@tailwindcss/postcss") {
        Write-Host " ALERTA: Encontrado @tailwindcss/postcss (Tailwind v4 plugin)" -ForegroundColor Red
    }

    if ($pkg -match '"tailwindcss"') {
        Write-Host " OK: Tailwind instalado" -ForegroundColor Green
    }

    if ($pkg -match '"craco"') {
        Write-Host " OK: CRACO encontrado" -ForegroundColor Green
    }
}

Write-Host ""

# ----------------------------------------------------------
# 7. Configs duplicadas
# ----------------------------------------------------------
Write-Host "7) Procurando configs duplicadas..." -ForegroundColor Yellow

Get-ChildItem . -Recurse -Include *tailwind*.js,*postcss*.js,*craco*.js |
ForEach-Object {
    Write-Host " CONFIG: $($_.FullName)" -ForegroundColor DarkYellow
}

Write-Host ""

# ----------------------------------------------------------
# 8. Resumo final
# ----------------------------------------------------------
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host " FIM DA AUDITORIA "
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Se aparecer ALERTA ou FALTA, me envie o resultado." -ForegroundColor White