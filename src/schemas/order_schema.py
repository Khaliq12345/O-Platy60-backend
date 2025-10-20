from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime


class OrderBase(BaseModel):
    ingredient_id: str
    quantity_ordered: float = Field(..., gt=0)
    quantity_received: Optional[float] = Field(None, ge=0)
    unit_price_ordered: float = Field(..., ge=0)
    unit_price_received: Optional[float] = Field(None, ge=0)
    notes: Optional[str] = None
    status: Literal['pending', 'confirmed', 'completed', 'cancelled'] = 'pending'
    value_ordered: float = Field(..., ge=0)
    value_received: Optional[float] = Field(None, ge=0)


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    ingredient_id: Optional[str] = None
    quantity_ordered: Optional[float] = Field(None, gt=0)
    quantity_received: Optional[float] = Field(None, ge=0)
    unit_price_ordered: Optional[float] = Field(None, ge=0)
    unit_price_received: Optional[float] = Field(None, ge=0)
    notes: Optional[str] = None
    status: Optional[Literal['pending', 'confirmed', 'completed', 'cancelled']] = None
    value_ordered: Optional[float] = Field(None, ge=0)
    value_received: Optional[float] = Field(None, ge=0)


class OrderResponse(OrderBase):
    id: int
    created_at: datetime
    completed_at: Optional[datetime] = None
    delete: bool = False

    class Config:
        from_attributes = True


class OrderWithIngredientResponse(BaseModel):
    id: int
    ingredient_id: str
    quantity_ordered: float
    quantity_received: Optional[float] = None
    unit_price_ordered: float
    unit_price_received: Optional[float] = None
    notes: Optional[str] = None
    status: str
    value_ordered: float
    value_received: Optional[float] = None
    created_at: datetime
    completed_at: Optional[datetime] = None
    delete: bool = False
    # Relation avec ingredient
    ingredients: Optional["IngredientResponse"] = None

    class Config:
        from_attributes = True


class OrderListResponse(BaseModel):
    orders: list[OrderWithIngredientResponse]
    total: int
    page: int
    limit: int
    has_next: bool
    has_prev: bool


class OrderFilter(BaseModel):
    status: str | None = None
    ingredient_id: Optional[str] = None
    delete: bool = False
    page: int = Field(1, ge=1)
    limit: int = Field(10, ge=1, le=100)


class IngredientBase(BaseModel):
    name: str
    category: Optional[str] = None
    current_stock_level: float = Field(0, ge=0)
    sku: Optional[str] = None
    unit: Optional[str] = None
    status: Optional[str] = None
    min_stock_level: float = Field(0, ge=0)
    storage_location: Optional[str] = None
    unit_cost: float = Field(0, ge=0)
    expire_at: Optional[datetime] = None
    value: float = Field(0, ge=0)


class IngredientCreate(IngredientBase):
    pass


class IngredientUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    current_stock_level: Optional[float] = Field(None, ge=0)
    sku: Optional[str] = None
    unit: Optional[str] = None
    status: Optional[str] = None
    min_stock_level: Optional[float] = Field(None, ge=0)
    storage_location: Optional[str] = None
    unit_cost: Optional[float] = Field(None, ge=0)
    expire_at: Optional[datetime] = None
    value: Optional[float] = Field(None, ge=0)


class IngredientResponse(BaseModel):
    sku: str
    name: str
    category: Optional[str] = None
    current_stock_level: float
    unit: Optional[str] = None
    status: Optional[str] = None
    min_stock_level: float
    storage_location: Optional[str] = None
    unit_cost: float
    expire_at: Optional[datetime] = None
    value: float
    created_at: datetime
    last_received: Optional[datetime] = None
    last_updated: Optional[datetime] = None
    delete: bool = False

    class Config:
        from_attributes = True


class StockAdjustment(BaseModel):
    order_id: int
    new_quantity_received: float = Field(..., ge=0)
    new_unit_price_received: float = Field(..., ge=0)
    reason: Optional[str] = None


class StockAdjustmentRequest(BaseModel):
    adjustments: list[StockAdjustment]