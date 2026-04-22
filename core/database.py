import os
from motor.motor_asyncio import AsyncIOMotorClient

# Variáveis globais para gerenciar a conexão
client: AsyncIOMotorClient = None
db = None

async def init_db():
    """Inicializa a conexão com o MongoDB"""
    global client, db
    mongo_url = os.environ.get("MONGO_URL", "mongodb://localhost:27017/consultslt_db")
    try:
        client = AsyncIOMotorClient(mongo_url)
        # Testa a conexão
        await client.admin.command('ping')
        db = client.get_database()
        print(f"INFO:     Conexão com MongoDB estabelecida com sucesso ({mongo_url})")
    except Exception as e:
        print(f"ERROR:    Falha ao conectar ao MongoDB: {e}")
        raise e

async def close_db():
    """Fecha a conexão com o MongoDB"""
    global client
    if client:
        client.close()
        print("INFO:     Conexão com MongoDB encerrada.")

def get_db():
    """Retorna a instância do banco de dados"""
    return db