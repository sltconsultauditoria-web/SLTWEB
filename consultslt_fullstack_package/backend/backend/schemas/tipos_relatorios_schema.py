from pydantic import BaseModel
from typing import Optional

class Tipos_relatoriosCreate(BaseModel):
    data: dict

class Tipos_relatoriosUpdate(BaseModel):
    data: Optional[dict]
    ativo: Optional[bool] = True

class Tipos_relatoriosSchema(Tipos_relatoriosCreate):
    id: str
    ativo: bool = True
