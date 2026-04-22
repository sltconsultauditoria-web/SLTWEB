# deploy.ps1
Write-Host "🔨 Gerando build otimizado..."
npm run build

Write-Host "🧹 Limpando pasta docs antiga..."
Remove-Item -Recurse -Force docs

Write-Host "📂 Movendo build para docs..."
Rename-Item build docs

Write-Host "📤 Fazendo commit e push para main..."
git add docs
git commit -m "Atualiza build para docs"
git push origin main

Write-Host "✅ Deploy concluído! Aguarde alguns minutos e acesse:"
Write-Host "https://sltconsultauditoria-web.github.io/SLTWEB/"
