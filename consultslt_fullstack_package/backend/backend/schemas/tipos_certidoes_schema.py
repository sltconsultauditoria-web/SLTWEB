from pydantic import BaseModel
from typing import Optional

class Tipos_certidoesCreate(BaseModel):
    data: dict

class Tipos_certidoesUpdate(BaseModel):
    data: Optional[dict]
    ativo: Optional[bool] = True

class Tipos_certidoesSchema(Tipos_certidoesCreate):
    id: str
    ativo: bool = True
