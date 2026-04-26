import os
import re
import importlib
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# ===============================
# CONFIG
# ===============================

BASE_DIR = Path(__file__).resolve().parent
ROUTERS_DIR = BASE_DIR / "backend" / "routers"
FRONTEND_DIR = BASE_DIR.parent / "frontend"

load_dotenv(BASE_DIR / ".env")

MONGO_URL = os.getenv("MONGO_URL", "mongodb://127.0.0.1:27017")
DB_NAME = os.getenv("MONGO_DB_NAME", "consultslt_db")

# ===============================
# CONEXÃO MONGO
# ===============================

async def get_existing_collections():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    collections = await db.list_collection_names()
    client.close()
    return collections

# ===============================
# ANALISADOR DE ROUTER
# ===============================

def analyze_router(file_path):
    content = file_path.read_text(encoding="utf-8")

    has_router = "APIRouter" in content and "router =" in content
    uses_get_db = "Depends(get_db)" in content
    imports_get_db = "get_db" in content
    has_routes = bool(re.search(r"@router\.(get|post|put|delete)", content))

    # tentativa de detectar coleção
    collection_match = re.findall(r"db\.([a-zA-Z_]+)", content)
    probable_collection = collection_match[0] if collection_match else None

    return {
        "has_router": has_router,
        "uses_get_db": uses_get_db,
        "imports_get_db": imports_get_db,
        "has_routes": has_routes,
        "collection": probable_collection,
    }

# ===============================
# FRONTEND SCAN
# ===============================

def frontend_calls(prefix):
    if not FRONTEND_DIR.exists():
        return False

    for file in FRONTEND_DIR.rglob("*.js"):
        content = file.read_text(encoding="utf-8", errors="ignore")
        if prefix in content:
            return True

    return False

# ===============================
# MAIN AUDIT
# ===============================

import asyncio

async def main():
    print("\n=== AUDITORIA DE COMUNICAÇÃO FULL STACK ===\n")

    collections = await get_existing_collections()

    for router_file in ROUTERS_DIR.glob("*.py"):
        if router_file.name == "__init__.py":
            continue

        prefix = f"/api/{router_file.stem}"
        analysis = analyze_router(router_file)

        print(f"\n🔎 Router: {router_file.stem}")
        print(f"   Prefix esperado: {prefix}")
        print(f"   APIRouter declarado: {'✅' if analysis['has_router'] else '❌'}")
        print(f"   Possui endpoints HTTP: {'✅' if analysis['has_routes'] else '❌'}")
        print(f"   Usa Depends(get_db): {'✅' if analysis['uses_get_db'] else '❌'}")
        print(f"   Importa get_db: {'✅' if analysis['imports_get_db'] else '❌'}")

        # Coleção Mongo
        if analysis["collection"]:
            exists = analysis["collection"] in collections
            print(f"   Coleção detectada: {analysis['collection']} -> {'✅ Existe' if exists else '❌ Não existe'}")
        else:
            print("   Coleção detectada: ❌ Não identificada")

        # Frontend
        frontend_exists = frontend_calls(prefix)
        print(f"   Frontend chama rota: {'✅' if frontend_exists else '❌'}")

    print("\n============================================\n")

if __name__ == "__main__":
    asyncio.run(main())