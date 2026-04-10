
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = "consultslt_db"

client = AsyncIOMotorClient(MONGO_URL)
database = client[DB_NAME]

def get_collection(name: str):
    return database[name]
