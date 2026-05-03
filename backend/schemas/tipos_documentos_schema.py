from pydantic import BaseModel, Field
from typing import Optional

class Tipos_documentosCreate(BaseModel):
    data: dict = Field(default_factory=dict)

class Tipos_documentosUpdate(BaseModel):
    data: Optional[dict] = None
    ativo: Optional[bool] = True

class Tipos_documentosSchema(Tipos_documentosCreate):
    id: str
    ativo: bool = True
