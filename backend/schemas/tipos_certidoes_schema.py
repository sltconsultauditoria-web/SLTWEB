from pydantic import BaseModel, Field
from typing import Optional

class Tipos_certidoesCreate(BaseModel):
    data: dict = Field(default_factory=dict)

class Tipos_certidoesUpdate(BaseModel):
    data: Optional[dict] = None
    ativo: Optional[bool] = True

class Tipos_certidoesSchema(Tipos_certidoesCreate):
    id: str
    ativo: bool = True
