# check_routes_with_db.py
import httpx
import re
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

BASE_URL = "http://localhost:8000"
MONGO_URL = "mongodb://localhost:27017"
DB_NAME = "consultslt_db"

async def get_collections():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    return await db.list_collection_names(), db

def extract_routes_from_main(file_path="backend/main_enterprise.py"):
    routes = []
    with open(file_path, encoding="utf-8") as f:
        content = f.read()
    matches = re.findall(r'prefix="(/api/[a-zA-Z0-9_]+)"', content)
    routes.extend(matches)
    return routes

async def check_routes(routes, collections, db):
    async with httpx.AsyncClient(timeout=5.0) as client:
        for route in routes:
            url = f"{BASE_URL}{route}/"
            collection_name = route.replace("/api/", "")

            print(f"\n🔎 Testando rota {route}...")

            try:
                r = await client.get(url)
                if r.status_code == 200:
                    try:
                        data = r.json()
                        if isinstance(data, list):
                            print(f"✅ {route} OK ({len(data)} registros)")
                        else:
                            print(f"✅ {route} OK (resposta JSON)")
                    except Exception:
                        print(f"✅ {route} OK (resposta não é JSON)")
                else:
                    print(f"❌ {route} retornou {r.status_code}")
            except Exception as e:
                print(f"⚠️ Erro ao acessar {route}: {e}")

            # Verifica coleção correspondente
            if collection_name in collections:
                count = await db[collection_name].count_documents({})
                print(f"   📂 Coleção '{collection_name}' existe com {count} documentos")
            else:
                print(f"   ⚠️ Coleção '{collection_name}' não encontrada no consultslt_db")

async def main():
    routes = extract_routes_from_main()
    print("📌 Rotas encontradas no main_enterprise.py:")
    for r in routes:
        print(" -", r)

    collections, db = await get_collections()
    print("\n📂 Coleções no consultslt_db:")
    for c in collections:
        print(" -", c)

    print("\n📊 Verificando rotas e coleções...\n")
    await check_routes(routes, collections, db)

if __name__ == "__main__":
    asyncio.run(main())
