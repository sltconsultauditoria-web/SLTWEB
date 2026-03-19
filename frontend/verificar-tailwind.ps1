Write-Host ""
Write-Host "======================================="
Write-Host "VERIFICACAO DE CONFIGURACAO TAILWIND"
Write-Host "======================================="
Write-Host ""

$patterns = @(
"tailwindcss",
"require('tailwindcss')",
'require("tailwindcss")',
"@tailwindcss/postcss"
)

$files = Get-ChildItem -Recurse -Include *.js,*.ts,*.jsx,*.tsx,*.json,*.css

foreach ($file in $files) {

    $content = Get-Content $file.FullName -Raw

    foreach ($pattern in $patterns) {

        if ($content -match $pattern) {

            Write-Host ""
            Write-Host "Arquivo:" $file.FullName -ForegroundColor Yellow
            Write-Host "Encontrado:" $pattern -ForegroundColor Red

            Select-String -Path $file.FullName -Pattern $pattern
        }
    }
}

Write-Host ""
Write-Host "======================================="
Write-Host "FIM DA VERIFICACAO"
Write-Host "======================================="