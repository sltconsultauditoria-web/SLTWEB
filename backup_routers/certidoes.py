
from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from backend.core.database import get_db
from bson import ObjectId

router = APIRouter()

COLLECTION = "certidoes"


@router.get("/")
async def listar(db: AsyncIOMotorDatabase = Depends(get_db)):
    data = await db[COLLECTION].find().to_list(100)
    for d in data:
        d["_id"] = str(d["_id"])
    return data


@router.get("/{id}")
async def obter(id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    data = await db[COLLECTION].find_one({"_id": ObjectId(id)})
    if data:
        data["_id"] = str(data["_id"])
    return data


@router.post("/")
async def criar(payload: dict, db: AsyncIOMotorDatabase = Depends(get_db)):
    result = await db[COLLECTION].insert_one(payload)
    return {"id": str(result.inserted_id)}


@router.put("/{id}")
async def atualizar(id: str, payload: dict, db: AsyncIOMotorDatabase = Depends(get_db)):
    await db[COLLECTION].update_one(
        {"_id": ObjectId(id)},
        {"$set": payload}
    )
    return {"status": "updated"}


@router.delete("/{id}")
async def deletar(id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    await db[COLLECTION].delete_one({"_id": ObjectId(id)})
    return {"status": "deleted"}
