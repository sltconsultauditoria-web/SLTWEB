# analyze_main_and_db.py
import re
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

MAIN_FILE = "backend/main_enterprise.py"
MONGO_URL = "mongodb://localhost:27017"
DB_NAME = "consultslt_db"

async def get_collections():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    return await db.list_collection_names()

def extract_routes_from_main(file_path=MAIN_FILE):
    with open(file_path, encoding="utf-8") as f:
        content = f.read()
    # captura prefixos /api/xxx
    matches = re.findall(r'prefix="(/api/[a-zA-Z0-9_]+)"', content)
    return matches

async def analyze():
    routes = extract_routes_from_main()
    collections = await get_collections()

    print("📌 Rotas encontradas no main_enterprise.py:")
    for r in routes:
        print(" -", r)

    print("\n📂 Coleções no consultslt_db:")
    for c in collections:
        print(" -", c)

    print("\n📊 Análise cruzada (rota ↔ coleção):\n")
    for route in routes:
        collection_name = route.replace("/api/", "")
        if collection_name in collections:
            print(f"✅ {route} → Coleção '{collection_name}' existe")
        else:
            print(f"⚠️ {route} → Coleção '{collection_name}' NÃO encontrada (remover router ou criar coleção)")

if __name__ == "__main__":
    asyncio.run(analyze())
