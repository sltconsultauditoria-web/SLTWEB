from pydantic import BaseModel
from typing import Optional

class Tipos_obrigacoesCreate(BaseModel):
    data: dict

class Tipos_obrigacoesUpdate(BaseModel):
    data: Optional[dict]
    ativo: Optional[bool] = True

class Tipos_obrigacoesSchema(Tipos_obrigacoesCreate):
    id: str
    ativo: bool = True
