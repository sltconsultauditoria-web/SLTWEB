from pydantic import BaseModel
from typing import Optional

class Relatorios_geradosCreate(BaseModel):
    data: dict

class Relatorios_geradosUpdate(BaseModel):
    data: Optional[dict]
    ativo: Optional[bool] = True

class Relatorios_geradosSchema(Relatorios_geradosCreate):
    id: str
    ativo: bool = True
