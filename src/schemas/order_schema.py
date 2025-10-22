from pydantic import BaseModel
from enum import Enum
from datetime import datetime

# Définir les énums
class OrderStatusEnum(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class INGREDIENT(BaseModel):
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
    
# Schéma unique pour les réponses ORDER
class ORDER(BaseModel):
    id: int | None = None
    created_at: str | None = None
    ingredient_id: str
    ingredients: INGREDIENT | None = None
    quantity_ordered: float | None = 0
    quantity_received: float | None = 0
    unit_price_ordered: float | None = 0
    unit_price_received: float | None = 0
    notes: str | None = None
    status: OrderStatusEnum
    value_ordered: float | None = 0
    value_received: float | None = 0
    completed_at: str | None = None
    delete: bool | None = False


