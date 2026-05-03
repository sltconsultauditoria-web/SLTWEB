from pydantic import BaseModel, Field
from typing import Optional

class Status_checksCreate(BaseModel):
    data: dict = Field(default_factory=dict)

class Status_checksUpdate(BaseModel):
    data: Optional[dict] = None
    ativo: Optional[bool] = True

class Status_checksSchema(Status_checksCreate):
    id: str
    ativo: bool = True
