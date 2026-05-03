# backend/core/mongo_db.py
import motor.motor_asyncio

MONGO_URL = "mongodb://localhost:27017"
DB_NAME = "consultslt_db"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

def get_db():
    """
    Retorna a instância do banco de dados MongoDB.
    """
    return db
