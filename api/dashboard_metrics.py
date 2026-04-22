from fastapi import APIRouter, HTTPException
from backend.schemas.dashboard_metrics import Dashboard_metricsCreate
from backend.repositories.dashboard_metrics_repository import *

router = APIRouter(prefix="/dashboard_metrics", tags=["dashboard_metrics"])

@router.post("/")
def create_item(data: Dashboard_metricsCreate):
    return {"id": create(data.model_dump())}

@router.get("/")
def list_items():
    return list_all()

@router.get("/{id}")
def get_item(id: str):
    item = get_by_id(id)
    if not item:
        raise HTTPException(404, "dashboard_metrics not found")
    return item

@router.put("/{id}")
def update_item(id: str, data: Dashboard_metricsCreate):
    return update(id, data.model_dump())

@router.delete("/{id}")
def delete_item(id: str):
    delete(id)
    return {"ok": True}