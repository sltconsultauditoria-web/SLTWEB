Write-Host "Iniciando limpeza de SQLAlchemy..." -ForegroundColor Cyan

$projectPath = ".\backend"
$backupPath = ".\backend_backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"

# Criar backup
Write-Host "Criando backup em $backupPath"
Copy-Item $projectPath $backupPath -Recurse -Force

# Palavras a remover
$patterns = @(
    "from sqlalchemy",
    "import sqlalchemy",
    "declarative_base",
    "ForeignKey",
    "Column",
    "create_engine"
)

# Percorrer arquivos Python
Get-ChildItem -Path $projectPath -Recurse -Filter "*.py" | ForEach-Object {

    $file = $_.FullName
    $content = Get-Content $file

    $newContent = $content | Where-Object {
        $line = $_
        $remove = $false

        foreach ($pattern in $patterns) {
            if ($line -match $pattern) {
                $remove = $true
            }
        }

        -not $remove
    }

    Set-Content -Path $file -Value $newContent
}

Write-Host "SQLAlchemy removido com sucesso." -ForegroundColor Green
Write-Host "Backup criado em: $backupPath"
