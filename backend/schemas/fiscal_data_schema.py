from pydantic import BaseModel, Field
from typing import Optional

class Fiscal_dataCreate(BaseModel):
    data: dict = Field(default_factory=dict)

class Fiscal_dataUpdate(BaseModel):
    data: Optional[dict] = None
    ativo: Optional[bool] = True

class Fiscal_dataSchema(Fiscal_dataCreate):
    id: str
    ativo: bool = True
