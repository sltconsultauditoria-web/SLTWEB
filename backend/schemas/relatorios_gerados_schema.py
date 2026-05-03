from pydantic import BaseModel, Field
from typing import Optional

class Relatorios_geradosCreate(BaseModel):
    data: dict = Field(default_factory=dict)

class Relatorios_geradosUpdate(BaseModel):
    data: Optional[dict] = None
    ativo: Optional[bool] = True

class Relatorios_geradosSchema(Relatorios_geradosCreate):
    id: str
    ativo: bool = True
