from pydantic import BaseModel
from typing import Optional

class Obrigacoes_empresaCreate(BaseModel):
    data: dict

class Obrigacoes_empresaUpdate(BaseModel):
    data: Optional[dict]
    ativo: Optional[bool] = True

class Obrigacoes_empresaSchema(Obrigacoes_empresaCreate):
    id: str
    ativo: bool = True
