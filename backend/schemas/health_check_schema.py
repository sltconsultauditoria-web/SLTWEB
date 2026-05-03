from pydantic import BaseModel, Field
from typing import Optional

class Health_checkCreate(BaseModel):
    data: dict = Field(default_factory=dict)

class Health_checkUpdate(BaseModel):
    data: Optional[dict] = None
    ativo: Optional[bool] = True

class Health_checkSchema(Health_checkCreate):
    id: str
    ativo: bool = True
