Write-Host "🚀 INICIANDO IMPLANTAÇÃO CONSULTSLT" -ForegroundColor Cyan

# ===============================
# 1️⃣ BACKUP
# ===============================
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
Copy-Item backend "backend_backup_$timestamp" -Recurse
Write-Host "✅ Backup criado: backend_backup_$timestamp"

# ===============================
# 2️⃣ ATIVAR VENV
# ===============================
if (!(Test-Path "venv")) {
    python -m venv venv
}
.\venv\Scripts\Activate.ps1
Write-Host "✅ Virtualenv ativo"

# ===============================
# 3️⃣ DEPENDÊNCIAS
# ===============================
pip install --upgrade pip
pip install fastapi uvicorn pymongo python-dotenv pydantic pytest
Write-Host "✅ Dependências instaladas"

# ===============================
# 4️⃣ VERIFICAR ROTAS REGISTRADAS
# ===============================
Write-Host "📌 Mapeando rotas..."
python scripts/map_routes.py

# ===============================
# 5️⃣ CRIAR COLEÇÕES NO MONGO
# ===============================
Write-Host "📦 Criando coleções no MongoDB..."
python scripts/init_collections.py

# ===============================
# 6️⃣ RODAR TESTES
# ===============================
Write-Host "🧪 Executando testes..."
pytest -q
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Testes falharam. Abortando deploy." -ForegroundColor Red
    exit 1
}
Write-Host "✅ Testes OK"

# ===============================
# 7️⃣ SUBIR API
# ===============================
Write-Host "🚀 Subindo API..."
uvicorn backend.main_enterprise:app --host 0.0.0.0 --port 8000 --reload
