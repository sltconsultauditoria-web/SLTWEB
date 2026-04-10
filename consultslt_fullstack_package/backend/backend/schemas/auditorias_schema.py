from pydantic import BaseModel
from typing import Optional

class AuditoriasCreate(BaseModel):
    data: dict

class AuditoriasUpdate(BaseModel):
    data: Optional[dict]
    ativo: Optional[bool] = True

class AuditoriasSchema(AuditoriasCreate):
    id: str
    ativo: bool = True
