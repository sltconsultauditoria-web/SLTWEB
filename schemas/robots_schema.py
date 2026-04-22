from pydantic import BaseModel
from typing import Optional

class RobotsCreate(BaseModel):
    data: dict

class RobotsUpdate(BaseModel):
    data: Optional[dict]
    ativo: Optional[bool] = True

class RobotsSchema(RobotsCreate):
    id: str
    ativo: bool = True
