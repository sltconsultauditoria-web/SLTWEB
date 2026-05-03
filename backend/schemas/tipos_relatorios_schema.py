from pydantic import BaseModel, Field
from typing import Optional

class Tipos_relatoriosCreate(BaseModel):
    data: dict = Field(default_factory=dict)

class Tipos_relatoriosUpdate(BaseModel):
    data: Optional[dict] = None
    ativo: Optional[bool] = True

class Tipos_relatoriosSchema(Tipos_relatoriosCreate):
    id: str
    ativo: bool = True
