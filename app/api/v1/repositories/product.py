from sqlalchemy.orm import Session
from app.api.v1.models.base import Product
from app.api.v1.models.ecommerce import EcommerceDBLayer
from app.api.v1.schemas.ecommerce import ProductCreate
from app.core.exception import CustomHTTPException


db_layer = EcommerceDBLayer()


class ProductRepository:

    @classmethod
    def get_products(cls, db: Session, skip, limit):
        products = db_layer.get_all(db, Product, skip, limit)
        if not products:
            raise CustomHTTPException(status_code=404, detail="No products available")
        return products

    @classmethod
    def add_product(cls, db: Session, product_data: ProductCreate):
        if product_data.price <= 0:
            raise CustomHTTPException(status_code=400, detail="Price must be greater than zero")
        if product_data.stock < 0:
            raise CustomHTTPException(status_code=400, detail="Stock cannot be negative")
        return db_layer.create_product(db, product_data)
