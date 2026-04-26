from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

# Configurações do MongoDB
MONGO_URI = "mongodb://localhost:27017"
DATABASE_NAME = "consultslt_db"
COLLECTION_NAME = "documentos"

async def clear_mocked_data():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DATABASE_NAME]
    
    # Remover todos os documentos da coleção
    result = await db[COLLECTION_NAME].delete_many({})
    print(f"{result.deleted_count} documentos mockados foram removidos.")

    # Fechar conexão com o banco de dados
    client.close()

if __name__ == "__main__":
    asyncio.run(clear_mocked_data())