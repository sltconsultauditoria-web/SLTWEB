from pydantic import BaseModel, Field
from typing import Optional

class Dashboard_metricsCreate(BaseModel):
    data: dict = Field(default_factory=dict)

class Dashboard_metricsUpdate(BaseModel):
    data: Optional[dict] = None
    ativo: Optional[bool] = True

class Dashboard_metricsSchema(Dashboard_metricsCreate):
    id: str
    ativo: bool = True
