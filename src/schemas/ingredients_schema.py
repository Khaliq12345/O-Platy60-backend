from pydantic import BaseModel
from datetime import datetime


class Ingredient(BaseModel):
    sku: str
    name: str
    category: str | None = None
    current_stock_level: float | None = 0
    unit: str | None = None
    status: str | None = None
    min_stock_level: float | None = 0
    storage_location: str | None = None
    last_received: datetime | None = None
    last_updated: datetime | None = None
    unit_cost: float | None = 0
    expire_at: datetime | None = None
    delete: bool | None = False
    value: float | None = 0
