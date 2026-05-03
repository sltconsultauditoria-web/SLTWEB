from pydantic import BaseModel, Field
from typing import Optional

class UsersCreate(BaseModel):
    data: dict = Field(default_factory=dict)

class UsersUpdate(BaseModel):
    data: Optional[dict] = None
    ativo: Optional[bool] = True

class UsersSchema(UsersCreate):
    id: str
    ativo: bool = True
