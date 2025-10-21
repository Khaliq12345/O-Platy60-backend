from pydantic import BaseModel
from datetime import datetime


class Ingredient(BaseModel):
    sku: str
    name: str
    category: str | None = None
    current_stock_level: float = 0.0
    unit: str
    status: str | None = None
    min_stock_level: float = 0.0
    storage_location: str | None = None
    last_received: str | None = None
    last_updated: str = datetime.now().isoformat()
    unit_cost: float
    expire_at: str | None = None
    delete: bool = False
    value: float = 0
