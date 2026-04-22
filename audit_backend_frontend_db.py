# audit_backend_frontend_db.py
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
    collections = await db.list_collection_names()
    return collections

def extract_routes_from_main(file_path="backend/main_enterprise.py"):
    routes = []
    with open(file_path, encoding="utf-8") as f:
        content = f.read()
    matches = re.findall(r'prefix="(/api/[a-zA-Z0-9_]+)"', content)
    routes.extend(matches)
    return routes

async def audit_routes(routes, collections):
    async with httpx.AsyncClient(timeout=5.0) as client:
        for route in routes:
            url = f"{BASE_URL}{route}"
            collection_name = route.replace("/api/", "")
            try:
                response = await client.get(url)
                if response.status_code == 200:
                    try:
                        data = response.json()
                        if isinstance(data, list):
                            print(f"✅ {route} OK ({len(data)} registros)")
                        else:
                            print(f"✅ {route} OK (resposta JSON)")
                    except Exception:
                        print(f"✅ {route} OK (resposta não é JSON)")
                else:
                    print(f"❌ {route} retornou {response.status_code}")
            except Exception as e:
                print(f"⚠️ Erro ao acessar {route}: {e}")

            # Verifica se coleção existe no banco
            if collection_name in collections:
                print(f"   📂 Coleção '{collection_name}' existe no consultslt_db")
            else:
                print(f"   ⚠️ Coleção '{collection_name}' não encontrada no consultslt_db")

async def main():
    routes = extract_routes_from_main()
    print("📌 Rotas encontradas no main_enterprise.py:")
    for r in routes:
        print(" -", r)

    collections = await get_collections()
    print("\n📂 Coleções no consultslt_db:")
    for c in collections:
        print(" -", c)

    print("\n📊 Testando rotas e coleções...\n")
    await audit_routes(routes, collections)

if __name__ == "__main__":
    asyncio.run(main())
