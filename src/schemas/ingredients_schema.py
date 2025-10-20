from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Ingredient(BaseModel):
    sku: str
    name: str
    category: Optional[str]
    current_stock_level: float
    unit: Optional[str]
    status: Optional[str]
    min_stock_level: float
    storage_location: Optional[str]
    last_received: Optional[datetime]
    last_updated: datetime
    unit_cost: float
    expire_at: Optional[datetime]
    delete: bool
    value: float

    class Config:
        orm_mode = True
