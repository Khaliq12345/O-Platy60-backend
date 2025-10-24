from pydantic import BaseModel


class Recipe(BaseModel):
    name: str
    category: str | None
    cost: float
    active: bool = True
    delete: bool = False
    last_updated: str | None = None
