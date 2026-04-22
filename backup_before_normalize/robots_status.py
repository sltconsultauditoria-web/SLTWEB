
from fastapi import APIRouter
# from database import db

router = APIRouter(prefix="/api/robots_status", tags=["robots_status"])

async def listar():
    from database import db
    return list(db["robots_status"].find({}, {"_id":0}))

async def criar(data: dict):
    from database import db
    db["robots_status"].insert_one(data)
    return {"status":"ok"}
