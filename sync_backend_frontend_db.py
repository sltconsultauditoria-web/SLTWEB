# sync_backend_frontend_db.py
import httpx
import re
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

BASE_URL = "http://localhost:8000"
MONGO_URL = "mongodb://localhost:27017"
DB_NAME = "consultslt_db"

# Documento de teste genérico
TEST_DOC = {
    "nome": "Registro de Teste",
    "descricao": "Documento inserido automaticamente para validar integração",
    "ativo": True
}

async def get_db():
    client = AsyncIOMotorClient(MONGO_URL)
    return client[DB_NAME]

def extract_routes_from_main(file_path="backend/main_enterprise.py"):
    routes = []
    with open(file_path, encoding="utf-8") as f:
        content = f.read()
    matches = re.findall(r'prefix="(/api/[a-zA-Z0-9_]+)"', content)
    routes.extend(matches)
    return routes

async def sync_routes(routes):
    db = await get_db()
    collections = await db.list_collection_names()

    async with httpx.AsyncClient(timeout=5.0) as client:
        for route in routes:
            url = f"{BASE_URL}{route}"
            collection_name = route.replace("/api/", "")

            print(f"\n🔎 Testando rota {route}...")

            # Testa rota
            try:
                response = await client.get(url)
                if response.status_code == 200:
                    print(f"✅ {route} OK")
                else:
                    print(f"❌ {route} retornou {response.status_code}")
            except Exception as e:
                print(f"⚠️ Erro ao acessar {route}: {e}")

            # Verifica coleção
            if collection_name in collections:
                count = await db[collection_name].count_documents({})
                if count == 0:
                    print(f"   ⚠️ Coleção '{collection_name}' está vazia. Inserindo documento de teste...")
                    await db[collection_name].insert_one(TEST_DOC)
                    print(f"   ✅ Documento de teste inserido em '{collection_name}'")
                else:
                    print(f"   📂 Coleção '{collection_name}' tem {count} documentos")
            else:
                print(f"   ⚠️ Coleção '{collection_name}' não encontrada no consultslt_db")

async def main():
    routes = extract_routes_from_main()
    print("📌 Rotas encontradas no main_enterprise.py:")
    for r in routes:
        print(" -", r)

    print("\n📊 Sincronizando rotas e coleções...\n")
    await sync_routes(routes)

if __name__ == "__main__":
    asyncio.run(main())
