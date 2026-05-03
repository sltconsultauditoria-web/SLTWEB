from pydantic import BaseModel
from typing import Optional

class AlertasBase(BaseModel):
    nome: Optional[str] = None

class AlertasCreate(AlertasBase):
    pass

class AlertasResponse(AlertasBase):
    id: str