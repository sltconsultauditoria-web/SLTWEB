from pydantic import BaseModel, Field
from typing import Optional

class RobotsCreate(BaseModel):
    data: dict = Field(default_factory=dict)

class RobotsUpdate(BaseModel):
    data: Optional[dict] = None
    ativo: Optional[bool] = True

class RobotsSchema(RobotsCreate):
    id: str
    ativo: bool = True
