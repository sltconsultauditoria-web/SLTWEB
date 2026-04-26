from fastapi import APIRouter, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient

router = APIRouter()

mongo_url = "mongodb://127.0.0.1:27017"
db_name = "consultslt_db"
client = AsyncIOMotorClient(mongo_url)
db = client[db_name]

@router.get("/generic/{collection_name}")
async def get_all_documents(collection_name: str):
    if collection_name not in await db.list_collection_names():
        raise HTTPException(status_code=404, detail="Collection not found")
    documents = await db[collection_name].find().to_list(100)
    return documents

@router.post("/generic/{collection_name}")
async def insert_document(collection_name: str, document: dict):
    if collection_name not in await db.list_collection_names():
        raise HTTPException(status_code=404, detail="Collection not found")
    result = await db[collection_name].insert_one(document)
    return {"inserted_id": str(result.inserted_id)}
