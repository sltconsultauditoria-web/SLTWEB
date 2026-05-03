from pydantic import BaseModel
from typing import Optional

class CertidoesBase(BaseModel):
    nome: Optional[str] = None

class CertidoesCreate(CertidoesBase):
    pass

class CertidoesResponse(CertidoesBase):
    id: str