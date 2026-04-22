
from fastapi import APIRouter
# from database import db

router = APIRouter(prefix="/api/tenants", tags=["tenants"])

@router.get("/")
async def listar():
    from database import db
    return list(db["tenants"].find({}, {"_id":0}))

@router.post("/")
async def criar(data: dict):
    from database import db
    db["tenants"].insert_one(data)
    return {"status":"ok"}
