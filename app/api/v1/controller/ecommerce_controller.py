from typing import List
from app.api.v1.models.base import get_db
from app.api.v1.schemas.ecommerce import OrderResponse, OrderCreate, ProductResponse, ProductCreate
from app.core.config import setup_logging
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.api.v1.repositories.product import ProductRepository
from app.api.v1.repositories.order import OrderRepository


logger = setup_logging(__name__)
router = APIRouter()

product_repository = ProductRepository()
order_repository = OrderRepository()


@router.get("/products", response_model=List[ProductResponse])
def get_products(db: Session = Depends(get_db),
                 skip: int = Query(0, ge=0, description="Number of items to skip"),
                 limit: int = Query(10, ge=1, le=100, description="Max number of items to return (1-100)")
    ):
    return product_repository.get_products(db, skip, limit)


@router.post("/products", response_model=ProductResponse)
def create_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    return product_repository.add_product(db, product_data)


@router.post("/orders", response_model=OrderResponse)
def create_order(order_data: OrderCreate, db: Session = Depends(get_db)):
    try:
        order = order_repository.place_order(db, order_data)
        return OrderResponse(id=order.id, total_price=order.total_price, status=order.status,
                             products=order_data.products)
    except Exception as err:
        raise err
