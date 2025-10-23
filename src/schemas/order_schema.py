from pydantic import BaseModel
from enum import Enum
from datetime import datetime
from src.schemas.ingredients_schema import Ingredient


# Définir les énums
class OrderStatusEnum(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


# Schéma unique pour les réponses ORDER
class ORDER(BaseModel):
    id: int | None = None
    created_at: str | None = None
    ingredient_id: str
    ingredients: Ingredient
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
