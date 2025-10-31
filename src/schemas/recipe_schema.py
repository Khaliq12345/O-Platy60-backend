from pydantic import BaseModel
from datetime import datetime


class Recipe(BaseModel):
    id: int | None = None
    name: str
    category: str | None = None
    cost: float
    active: bool | None = True
    delete: bool | None = False
    last_updated: datetime | None = None
