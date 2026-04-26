from pydantic import BaseModel
from typing import Optional

class Dashboard_metricsCreate(BaseModel):
    data: dict

class Dashboard_metricsUpdate(BaseModel):
    data: Optional[dict]
    ativo: Optional[bool] = True

class Dashboard_metricsSchema(Dashboard_metricsCreate):
    id: str
    ativo: bool = True
