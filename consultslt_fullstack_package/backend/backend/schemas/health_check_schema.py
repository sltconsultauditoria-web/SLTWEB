from pydantic import BaseModel
from typing import Optional

class Health_checkCreate(BaseModel):
    data: dict

class Health_checkUpdate(BaseModel):
    data: Optional[dict]
    ativo: Optional[bool] = True

class Health_checkSchema(Health_checkCreate):
    id: str
    ativo: bool = True
