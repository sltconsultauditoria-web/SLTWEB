from pydantic import BaseModel
from typing import Optional

class AlertasCreate(BaseModel):
    data: dict

class AlertasUpdate(BaseModel):
    data: Optional[dict]
    ativo: Optional[bool] = True

class AlertasSchema(AlertasCreate):
    id: str
    ativo: bool = True
