from fastapi import APIRouter, HTTPException
from backend.dashboard_metrics import Dashboard_metricsCreate
from backend.repositories.dashboard_metrics_repository import *

router = APIRouter(prefix="/api/dashboard_metrics", tags=["Dashboard Metrics"])

@router.post("/")
def create_item(data: Dashboard_metricsCreate):
    return {"id": create(data.model_dump())}

@router.get("/")
def list_items():
    return mongo_list_to_dict_list(list_all())

@router.get("/{id}")
def get_item(id: str):
    item = get_by_id(id)
    if not item:
        raise HTTPException(404, "dashboard_metrics not found")
    return mongo_list_to_dict_list([item])[0]

@router.put("/{id}")
def update_item(id: str, data: Dashboard_metricsCreate):
    updated_item = update(id, data.model_dump())
    return mongo_list_to_dict_list([updated_item])[0]

@router.delete("/{id}")
def delete_item(id: str):
    delete(id)
    return {"ok": True}