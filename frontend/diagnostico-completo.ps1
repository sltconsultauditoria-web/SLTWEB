Write-Host "==============================="
Write-Host "DIAGNOSTICO FRONTEND REACT"
Write-Host "==============================="

# 1. Node e NPM
Write-Host "`n[1] Versoes:"
node -v
npm -v

# 2. Verificar React
Write-Host "`n[2] React instalado:"
npm ls react react-dom --depth=0

# 3. Verificar React Router
Write-Host "`n[3] React Router:"
npm ls react-router-dom --depth=0

# 4. Verificar Tailwind / PostCSS
Write-Host "`n[4] Tailwind / PostCSS:"
npm ls tailwindcss postcss autoprefixer @tailwindcss/postcss --depth=0

# 5. Verificar erros no build
Write-Host "`n[5] Testando build:"
npm run build

# 6. Verificar porta 3000
Write-Host "`n[6] Porta 3000 em uso:"
netstat -ano | findstr :3000

# 7. Testar backend (ajuste se necessário)
Write-Host "`n[7] Testando API backend:"
try {
    Invoke-WebRequest -Uri "http://localhost:8080" -UseBasicParsing -TimeoutSec 5
    Write-Host "Backend OK"
} catch {
    Write-Host "Backend NAO respondeu"
}

# 8. Verificar arquivos críticos
Write-Host "`n[8] Verificando arquivos importantes:"
$files = @(
    "src\App.js",
    "src\index.js",
    "src\index.css",
    "tailwind.config.js",
    "postcss.config.js"
)

foreach ($file in $files) {
    if (Test-Path $file) {
        Write-Host "$file OK"
    } else {
        Write-Host "$file NAO encontrado"
    }
}

# 9. Limpeza opcional
Write-Host "`n[9] Sugestao limpeza:"
Write-Host "Execute manualmente se necessario:"
Write-Host "rm -rf node_modules"
Write-Host "del package-lock.json"
Write-Host "npm install"

Write-Host "`n==============================="
Write-Host "FIM DO DIAGNOSTICO"
Write-Host "==============================="