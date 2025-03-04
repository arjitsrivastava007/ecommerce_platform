from pydantic import BaseModel
from typing import List


# Pydantic Schemas
class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    stock: int


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int


class OrderCreate(BaseModel):
    products: List[OrderItemBase]


class OrderResponse(BaseModel):
    id: int
    total_price: float
    status: str
    products: List[OrderItemBase]

    class Config:
        from_attributes = True
