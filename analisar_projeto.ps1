Write-Host "============================="
Write-Host "DIAGNOSTICO DO PROJETO SLTWEB"
Write-Host "============================="

$root = Get-Location

Write-Host "`nDiretório atual:" $root

# 1 Verificar ferramentas instaladas
Write-Host "`nVerificando ferramentas..."

$tools = @("node","npm","python","pip","docker","git")

foreach ($tool in $tools) {
    $exists = Get-Command $tool -ErrorAction SilentlyContinue
    if ($exists) {
        Write-Host "$tool OK"
    } else {
        Write-Host "$tool NAO INSTALADO"
    }
}

# 2 Detectar projetos
Write-Host "`nDetectando tipos de projeto..."

if (Test-Path "frontend/package.json") {
    Write-Host "Frontend React detectado"
}

if (Test-Path "backend/requirements.txt") {
    Write-Host "Backend Python detectado"
}

if (Test-Path "docker-compose.yml") {
    Write-Host "Docker Compose configurado"
}

# 3 Listar diretórios grandes
Write-Host "`nPastas grandes (>100MB):"

Get-ChildItem -Directory -Recurse |
ForEach-Object {
    $size = (Get-ChildItem $_.FullName -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
    if ($size -gt 100MB) {
        "{0} - {1:N2} MB" -f $_.FullName, ($size/1MB)
    }
}

# 4 Detectar backups
Write-Host "`nPossiveis backups para limpeza:"

Get-ChildItem -Recurse -Directory |
Where-Object {
    $_.Name -match "backup|old|temp|copy"
} | Select-Object FullName

# 5 Detectar node_modules
Write-Host "`nNode modules encontrados:"

Get-ChildItem -Recurse -Directory |
Where-Object { $_.Name -eq "node_modules" } |
Select-Object FullName

# 6 Detectar builds antigos
Write-Host "`nBuilds detectados:"

$buildFolders = @("build","dist","docs")

foreach ($folder in $buildFolders) {
    Get-ChildItem -Recurse -Directory |
    Where-Object { $_.Name -eq $folder } |
    Select-Object FullName
}

Write-Host "`nAnalise concluida."