
from fastapi import APIRouter
# from database import db

router = APIRouter(prefix="/api/dashboard_snapshots", tags=["dashboard_snapshots"])

@router.get("/")
async def listar():
    from database import db
    return list(db["dashboard_snapshots"].find({}, {"_id":0}))

@router.post("/")
async def criar(data: dict):
    from database import db
    db["dashboard_snapshots"].insert_one(data)
    return {"status":"ok"}
