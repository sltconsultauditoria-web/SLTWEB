from pydantic import BaseModel, Field
from typing import Optional

class CertidoesCreate(BaseModel):
    data: dict = Field(default_factory=dict)

class CertidoesUpdate(BaseModel):
    data: Optional[dict] = None
    ativo: Optional[bool] = True

class CertidoesSchema(CertidoesCreate):
    id: str
    ativo: bool = True
