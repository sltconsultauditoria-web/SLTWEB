from pydantic import BaseModel
from typing import Optional

class Status_checksCreate(BaseModel):
    data: dict

class Status_checksUpdate(BaseModel):
    data: Optional[dict]
    ativo: Optional[bool] = True

class Status_checksSchema(Status_checksCreate):
    id: str
    ativo: bool = True
