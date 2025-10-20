from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# Schéma unique pour les réponses ORDER
class ORDER(BaseModel):
    id: int
    created_at: datetime
    ingredient_id: Optional[str] = None
    quantity_ordered: Optional[float] = None
    quantity_received: Optional[float] = None
    unit_price_ordered: Optional[float] = None
    unit_price_received: Optional[float] = None
    notes: Optional[str] = None
    status: Optional[str] = None
    value_ordered: Optional[float] = None
    value_received: Optional[float] = None
    completed_at: Optional[datetime] = None
    delete: Optional[bool] = None

    class Config:
        from_attributes = True


# Réponse pour les listes paginées
class OrderListResponse(BaseModel):
    orders: list[ORDER]
    total: int
    page: int
    limit: int
    has_next: bool
    has_prev: bool
