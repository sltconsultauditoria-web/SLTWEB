from pydantic import BaseModel, Field
from typing import Optional

class AlertasCreate(BaseModel):
    data: dict = Field(default_factory=dict)

class AlertasUpdate(BaseModel):
    data: Optional[dict] = None
    ativo: Optional[bool] = True

class AlertasSchema(AlertasCreate):
    id: str
    ativo: bool = True
