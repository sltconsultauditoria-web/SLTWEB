# sync-docs.ps1
Write-Host "Verificando arquivos de build e docs..."

# Pega todos os arquivos da pasta build
$buildFiles = Get-ChildItem -Recurse .\build

# Pega todos os arquivos da pasta docs
$docsFiles = Get-ChildItem -Recurse .\docs

# Normaliza os nomes (só o nome do arquivo)
$buildNames = $buildFiles | ForEach-Object { Split-Path $_.FullName -Leaf }
$docsNames = $docsFiles | ForEach-Object { Split-Path $_.FullName -Leaf }

# Descobre quais arquivos estão em build mas não em docs
$missing = $buildFiles | Where-Object { (Split-Path $_.FullName -Leaf) -notin $docsNames }

if ($missing) {
    Write-Host "`nArquivos que estão em build mas faltam em docs:"
    $missing | ForEach-Object { Write-Host " - " (Split-Path $_.FullName -Leaf) }

    Write-Host "`nCopiando arquivos faltantes para docs..."
    foreach ($file in $missing) {
        $relativePath = $file.FullName.Substring((Get-Item .\build).FullName.Length)
        $targetPath = Join-Path (Get-Item .\docs).FullName $relativePath

        # Cria diretório se não existir
        $targetDir = Split-Path $targetPath -Parent
        if (-not (Test-Path $targetDir)) {
            New-Item -ItemType Directory -Force -Path $targetDir | Out-Null
        }

        # Copia o arquivo
        Copy-Item $file.FullName $targetPath -Force
    }

    Write-Host "`nArquivos faltantes foram copiados para docs."
} else {
    Write-Host "`nTodos os arquivos de build já estão em docs."
}
