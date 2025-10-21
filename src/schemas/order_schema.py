from pydantic import BaseModel
from enum import Enum


# Définir les énums
class OrderStatusEnum(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


# Schéma unique pour les réponses ORDER
class ORDER(BaseModel):
    ingredient_id: str
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
