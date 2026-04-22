from pydantic import BaseModel
from typing import Optional

class EmpresasCreate(BaseModel):
    data: dict

class EmpresasUpdate(BaseModel):
    data: Optional[dict]
    ativo: Optional[bool] = True

class EmpresasSchema(EmpresasCreate):
    id: str
    ativo: bool = True
