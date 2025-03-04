from sqlalchemy.orm import Session
from app.api.v1.models.base import Product
from app.api.v1.models.ecommerce import EcommerceDBLayer
from app.core.exception import CustomHTTPException
from app.api.v1.schemas.ecommerce import OrderCreate


db_layer = EcommerceDBLayer()


class OrderRepository:

    @classmethod
    def place_order(cls, db: Session, order_data: OrderCreate):
        if not order_data.products:
            raise CustomHTTPException(status_code=400, detail="Order must contain at least one product")

        errors = []
        request_products = {item.product_id: item for item in order_data.products}
        product_ids = [item.product_id for item in order_data.products]

        # Fetch all products in one query (Optimized)
        products = {product.id: product for product in db_layer.filter_by_item_ids(db, Product, product_ids)}

        if len(products) != len(request_products):
            missing_products = set(request_products) - set(products.keys())
            errors.append(f"Products not found: {missing_products}")

        for product_id, product in products.items():
            if request_products[product_id].quantity <= 0:
                errors.append(f"Product quantitiy cannot be less than or equals 0")
            if product.stock < request_products[product_id].quantity:
                errors.append(f"Insufficient stock for product - {product.id}, name - {product.name}, "
                              f"stock - {product.stock}")

        if errors:
            raise CustomHTTPException(status_code=400, detail="Invalid details supplied for product",
                                      payload=order_data.dict(), errors=errors)

        return db_layer.create_order(db, order_data, products)
