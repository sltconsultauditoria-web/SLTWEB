from pydantic import BaseModel, Field
from typing import Optional

class FiscalCreate(BaseModel):
    data: dict = Field(default_factory=dict)

class FiscalUpdate(BaseModel):
    data: Optional[dict] = None
    ativo: Optional[bool] = True

class FiscalSchema(FiscalCreate):
    id: str
    ativo: bool = True
