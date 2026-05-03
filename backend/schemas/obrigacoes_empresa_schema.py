from pydantic import BaseModel, Field
from typing import Optional

class Obrigacoes_empresaCreate(BaseModel):
    data: dict = Field(default_factory=dict)

class Obrigacoes_empresaUpdate(BaseModel):
    data: Optional[dict] = None
    ativo: Optional[bool] = True

class Obrigacoes_empresaSchema(Obrigacoes_empresaCreate):
    id: str
    ativo: bool = True
