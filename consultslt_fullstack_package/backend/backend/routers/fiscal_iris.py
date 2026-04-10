
from fastapi import APIRouter
# from database import db

router = APIRouter(prefix="/api/fiscal_iris", tags=["fiscal_iris"])

@router.get("/")
async def listar():
    from database import db
    return list(db["fiscal_iris"].find({}, {"_id":0}))

@router.post("/")
async def criar(data: dict):
    from database import db
    db["fiscal_iris"].insert_one(data)
    return {"status":"ok"}
