from pydantic import BaseModel
from typing import Optional

class FiscalCreate(BaseModel):
    data: dict

class FiscalUpdate(BaseModel):
    data: Optional[dict]
    ativo: Optional[bool] = True

class FiscalSchema(FiscalCreate):
    id: str
    ativo: bool = True
