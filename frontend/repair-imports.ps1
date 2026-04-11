Write-Host ""
Write-Host "======================================"
Write-Host "REPARO DE IMPORTS REACT (@ ALIAS)"
Write-Host "======================================"
Write-Host ""

# Caminho do projeto
$srcPath = "src"

if (!(Test-Path $srcPath)) {
    Write-Host "ERRO: pasta src nao encontrada"
    exit
}

Write-Host "1) Verificando craco.config.js..."

$cracoFile = "craco.config.js"

if (!(Test-Path $cracoFile)) {

    Write-Host "craco.config.js nao encontrado, criando..."

$cracoContent = @"
const path = require("path");

module.exports = {
  webpack: {
    alias: {
      "@": path.resolve(__dirname, "src"),
    },
  },
  style: {
    postcss: {
      plugins: [
        require("tailwindcss"),
        require("autoprefixer"),
      ],
    },
  },
};
"@

    Set-Content $cracoFile $cracoContent

}
else {

    $content = Get-Content $cracoFile -Raw

    if ($content -notmatch "alias") {

        Write-Host "Alias @ nao encontrado, corrigindo..."

$fix = @"
const path = require("path");

module.exports = {
  webpack: {
    alias: {
      "@": path.resolve(__dirname, "src"),
    },
  },
};
"@

        Set-Content $cracoFile $fix
    }
    else {
        Write-Host "Alias @ ja configurado"
    }

}

Write-Host ""
Write-Host "2) Escaneando imports no projeto..."

$files = Get-ChildItem $srcPath -Recurse -Include *.js,*.jsx,*.ts,*.tsx

$brokenImports = @()

foreach ($file in $files) {

    $lines = Get-Content $file.FullName

    foreach ($line in $lines) {

        if ($line -match "@/") {

            $importPath = $line.Split('"')[1]

            $relative = $importPath.Replace("@/", "")

            $check1 = Join-Path $srcPath $relative
            $check2 = "$check1.js"
            $check3 = "$check1.jsx"
            $check4 = "$check1.tsx"

            if (!(Test-Path $check1) -and !(Test-Path $check2) -and !(Test-Path $check3) -and !(Test-Path $check4)) {

                $brokenImports += "$($file.FullName) -> $importPath"

            }

        }

    }

}

Write-Host ""
Write-Host "3) Resultado da analise"
Write-Host ""

if ($brokenImports.Count -eq 0) {

    Write-Host "Nenhum import quebrado encontrado"

}
else {

    Write-Host "IMPORTS QUEBRADOS:"
    Write-Host ""

    foreach ($b in $brokenImports) {
        Write-Host $b
    }

}

Write-Host ""
Write-Host "4) Testando build..."

npm run build

if ($LASTEXITCODE -eq 0) {

    Write-Host ""
    Write-Host "======================================"
    Write-Host "BUILD OK"
    Write-Host "======================================"

}
else {

    Write-Host ""
    Write-Host "======================================"
    Write-Host "BUILD AINDA FALHOU"
    Write-Host "Verifique imports listados acima"
    Write-Host "======================================"

}
