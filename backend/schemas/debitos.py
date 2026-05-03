from pydantic import BaseModel
from typing import Optional

class DebitosBase(BaseModel):
    nome: Optional[str] = None

class DebitosCreate(DebitosBase):
    pass

class DebitosResponse(DebitosBase):
    id: str