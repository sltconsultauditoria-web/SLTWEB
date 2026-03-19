Write-Host "🧹 Limpando estrutura duplicada..."

$folders = @(
    "backend\api",
    "backend\modules",
    "backend\src",
    "backend_backup_20260217_132052",
    "backend_backup_20260218_213452",
    "backend_backup_20260218_215555",
    "analysis"
)

foreach ($folder in $folders) {
    if (Test-Path $folder) {
        Remove-Item $folder -Recurse -Force
        Write-Host "❌ Removido: $folder"
    }
}

Write-Host "✅ Projeto limpo com sucesso!"
