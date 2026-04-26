from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

async def list_collections():
    mongo_url = "mongodb://127.0.0.1:27017"  # Atualize se necessário
    db_name = "consultslt_db"

    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]

    collections = await db.list_collection_names()
    print("Coleções no banco de dados:")
    for collection in collections:
        print(f"- {collection}")

    client.close()

if __name__ == "__main__":
    asyncio.run(list_collections())