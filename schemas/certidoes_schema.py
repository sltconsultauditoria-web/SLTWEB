from pydantic import BaseModel
from typing import Optional

class CertidoesCreate(BaseModel):
    data: dict

class CertidoesUpdate(BaseModel):
    data: Optional[dict]
    ativo: Optional[bool] = True

class CertidoesSchema(CertidoesCreate):
    id: str
    ativo: bool = True
