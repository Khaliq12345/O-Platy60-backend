from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class AdjustmentType(Enum):
    waste = "waste"
    received = "received"
    manual_count = "manual_count"
    recipe_usage = "recipe_usage"


class WasteCategory(Enum):
    spoilage = "spoilage"
    preparation = "preparation"
    dropped = "dropped"
    expired = "expired"


class Ingredient(BaseModel):
    sku: str
    name: str
    created_at: str | None = None
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


class Stock_Adjustment(BaseModel):
    ingredient_sku: str
    adjustment_type: AdjustmentType
    quantity_change: float | int
    reason: str
    waste_category: WasteCategory
    notes: str | None
    evidence_url: str | None
    cost_impact: float
    adjusted_by: str | None
    order_id: int | None
    recipe_id: int | None
