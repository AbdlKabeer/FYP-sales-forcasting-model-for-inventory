from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Product Schemas


class ProductBase(BaseModel):
    name: str
    category: str
    cost_price: float
    selling_price: float
    stock_quantity: int


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

# Sale Schemas


class SaleBase(BaseModel):
    product_id: int
    quantity: int


class SaleCreate(SaleBase):
    sale_date: Optional[datetime] = None


class Sale(SaleBase):
    id: int
    total_amount: float
    sale_date: datetime

    class Config:
        orm_mode = True

# Budget Schemas


class BudgetBase(BaseModel):
    category: str
    amount_limit: float
    period_start: datetime
    period_end: datetime


class BudgetCreate(BudgetBase):
    pass


class Budget(BudgetBase):
    id: int
    current_spend: float

    class Config:
        orm_mode = True

# Forecast Schemas


class ForecastRequest(BaseModel):
    product_id: int
    days: int = 30
    model_type: str = "linear"  # "linear" or "sarima"


class ForecastPoint(BaseModel):
    date: datetime
    predicted_quantity: float

class ForecastMetrics(BaseModel):
    training_rmse: float
    training_mae: float
    r2_score: float

class ForecastResponse(BaseModel):
    forecast: List[ForecastPoint]
    metrics: ForecastMetrics
