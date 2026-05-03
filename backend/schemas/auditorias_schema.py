from pydantic import BaseModel, Field
from typing import Optional

class AuditoriasCreate(BaseModel):
    data: dict = Field(default_factory=dict)

class AuditoriasUpdate(BaseModel):
    data: Optional[dict] = None
    ativo: Optional[bool] = True

class AuditoriasSchema(AuditoriasCreate):
    id: str
    ativo: bool = True
