
from fastapi import APIRouter
# from database import db

router = APIRouter(prefix="/api/tenants", tags=["tenants"])

async def listar():
    from database import db
    return list(db["tenants"].find({}, {"_id":0}))

async def criar(data: dict):
    from database import db
    db["tenants"].insert_one(data)
    return {"status":"ok"}
