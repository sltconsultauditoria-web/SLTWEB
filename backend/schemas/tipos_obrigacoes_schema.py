from pydantic import BaseModel, Field
from typing import Optional

class Tipos_obrigacoesCreate(BaseModel):
    data: dict = Field(default_factory=dict)

class Tipos_obrigacoesUpdate(BaseModel):
    data: Optional[dict] = None
    ativo: Optional[bool] = True

class Tipos_obrigacoesSchema(Tipos_obrigacoesCreate):
    id: str
    ativo: bool = True
