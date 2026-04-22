from pydantic import BaseModel
from typing import Optional

class Fiscal_dataCreate(BaseModel):
    data: dict

class Fiscal_dataUpdate(BaseModel):
    data: Optional[dict]
    ativo: Optional[bool] = True

class Fiscal_dataSchema(Fiscal_dataCreate):
    id: str
    ativo: bool = True
