from pydantic import BaseModel, Field
from typing import Optional

class EmpresasCreate(BaseModel):
    data: dict = Field(default_factory=dict)

class EmpresasUpdate(BaseModel):
    data: Optional[dict] = None
    ativo: Optional[bool] = True

class EmpresasSchema(EmpresasCreate):
    id: str
    ativo: bool = True
