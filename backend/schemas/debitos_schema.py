from pydantic import BaseModel
from typing import Optional

class DebitosCreate(BaseModel):
    data: dict

class DebitosUpdate(BaseModel):
    data: Optional[dict]
    ativo: Optional[bool] = True

class DebitosSchema(DebitosCreate):
    id: str
    ativo: bool = True
