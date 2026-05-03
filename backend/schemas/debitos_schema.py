from pydantic import BaseModel, Field
from typing import Optional

class DebitosCreate(BaseModel):
    data: dict = Field(default_factory=dict)

class DebitosUpdate(BaseModel):
    data: Optional[dict] = None
    ativo: Optional[bool] = True

class DebitosSchema(DebitosCreate):
    id: str
    ativo: bool = True
