from fastapi import APIRouter

from backend.core.database import get_db


router = APIRouter(prefix="/api/ecac", tags=["ecac"])
db = get_db()


@router.get("/")
async def list_ecac():
    items = await db["ecac"].find({"ativo": {"$ne": False}}).to_list(100)
    return [{**{k: v for k, v in item.items() if k != "_id"}, "id": str(item.get("_id"))} for item in items]


@router.get("/status")
async def ecac_status():
    return {"status": "ok", "modo": "mongo"}
