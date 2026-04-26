# enterprise_cleanup_validate.py
import os
import sys
from pathlib import Path
import subprocess
import shutil

BASE_DIR = Path(__file__).parent.resolve()
BACKEND_DIR = BASE_DIR / "backend"
CORE_DIR = BACKEND_DIR / "core"
ROUTERS_DIR = BACKEND_DIR / "routers"

print("🚀 INICIANDO LIMPEZA E VALIDAÇÃO FINAL DO PROJETO")

# 1️⃣ Garantir __init__.py em backend/core e routers
for folder in [BACKEND_DIR, CORE_DIR, ROUTERS_DIR]:
    init_file = folder / "__init__.py"
    if not init_file.exists():
        print(f"📄 Criando {init_file}")
        init_file.touch()
    else:
        print(f"✅ {init_file} já existe")

# 2️⃣ Corrigir imports nos routers (from backend.database → from backend.core.database)
print("🔧 Corrigindo imports internos nos routers...")
for py_file in ROUTERS_DIR.rglob("*.py"):
    with open(py_file, "r", encoding="utf-8") as f:
        content = f.read()
    if "from backend.database" in content:
        content = content.replace("from backend.database", "from backend.core.database")
        with open(py_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Corrigido import em {py_file}")

# 3️⃣ Garantir backend/core/database.py com MongoDB (Motor)
DB_FILE = CORE_DIR / "database.py"
if not DB_FILE.exists():
    print(f"⚠️ {DB_FILE} não existe, criando versão mínima MongoDB...")
    DB_FILE.write_text(
        """from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URL)
db = client["consultslt_db"]
"""
    )
    print(f"✅ Criado {DB_FILE}")
else:
    print(f"✅ {DB_FILE} já existe")

# 4️⃣ Validar que FastAPI e Motor estão instalados
print("📦 Validando dependências Python...")
for pkg in ["fastapi", "uvicorn", "motor"]:
    try:
        __import__(pkg)
        print(f"✅ Pacote {pkg} instalado")
    except ImportError:
        print(f"❌ Pacote {pkg} não encontrado. Instalando...")
        subprocess.run([sys.executable, "-m", "pip", "install", pkg])

# 5️⃣ Testar conexão com MongoDB
print("🔎 Testando conexão com MongoDB...")
try:
    from backend.core import database
    db = database.db
    result = db.list_collection_names()
    print(f"✅ MongoDB conectado, coleções encontradas: {result}")
except Exception as e:
    print(f"❌ Falha na conexão MongoDB: {e}")

# 6️⃣ Testar rotas FastAPI básicas
print("🔎 Validando rota / do FastAPI...")
try:
    import asyncio
    from fastapi.testclient import TestClient
    from backend.main_enterprise import app

    client = TestClient(app)
    response = client.get("/")
    if response.status_code == 200:
        print(f"✅ Rota / funcionando: {response.json()}")
    else:
        print(f"❌ Rota / retornou {response.status_code}: {response.text}")
except Exception as e:
    print(f"❌ Falha ao testar FastAPI: {e}")

print("🎯 LIMPEZA E VALIDAÇÃO FINAL CONCLUÍDA")
print("💡 Agora você deve conseguir subir o backend sem erros:")
print("$env:PYTHONPATH='.'; uvicorn backend.main_enterprise:app --host 0.0.0.0 --reload")
