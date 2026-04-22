
from fastapi import APIRouter
# from database import db

router = APIRouter(prefix="/api/sharepoint_status", tags=["sharepoint_status"])

@router.get("/")
async def listar():
    from database import db
    return list(db["sharepoint_status"].find({}, {"_id":0}))

@router.post("/")
async def criar(data: dict):
    from database import db
    db["sharepoint_status"].insert_one(data)
    return {"status":"ok"}
