from pydantic import BaseModel
from typing import Optional

class Dashboard_metricsBase(BaseModel):
    nome: Optional[str] = None

class Dashboard_metricsCreate(Dashboard_metricsBase):
    pass

class Dashboard_metricsResponse(Dashboard_metricsBase):
    id: str