from pydantic import BaseModel
from typing import Optional

class UsersCreate(BaseModel):
    data: dict

class UsersUpdate(BaseModel):
    data: Optional[dict]
    ativo: Optional[bool] = True

class UsersSchema(UsersCreate):
    id: str
    ativo: bool = True
