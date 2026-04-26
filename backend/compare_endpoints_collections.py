from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import os
import re

async def list_collections():
    mongo_url = "mongodb://127.0.0.1:27017"  # Atualize se necessário
    db_name = "consultslt_db"

    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]

    collections = await db.list_collection_names()
    client.close()
    return collections

def extract_endpoints():
    routers_path = "c:/Users/admin-local/ServerApp/SLTWEB/consultSLTweb/backend/routers"
    endpoints = []

    for root, _, files in os.walk(routers_path):
        for file in files:
            if file.endswith(".py"):
                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                    content = f.read()
                    matches = re.findall(r"@router\.(?:get|post|put|delete)\(\"(.*?)\"", content)
                    endpoints.extend(matches)

    return [endpoint.strip("/") for endpoint in endpoints]

async def compare():
    collections = await list_collections()
    endpoints = extract_endpoints()

    print("Coleções no MongoDB:")
    print(collections)
    print("\nEndpoints definidos:")
    print(endpoints)

    print("\nColeções sem endpoints correspondentes:")
    print(set(collections) - set(endpoints))

    print("\nEndpoints sem coleções correspondentes:")
    print(set(endpoints) - set(collections))

if __name__ == "__main__":
    asyncio.run(compare())