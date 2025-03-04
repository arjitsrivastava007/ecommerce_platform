import traceback
from typing import Dict
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.api.v1.models.base import Product, Order, OrderItem, Base
from app.api.v1.schemas.ecommerce import ProductCreate, OrderCreate
from app.core.exception import CustomHTTPException


class EcommerceDBLayer:
    def get_all(self, db: Session, model: Base, skip, limit):
        """
        Get all objects from Model
        :param db:
        :param model:
        :return:
        """
        return db.query(model).offset(skip).limit(limit).all()

    def get_item_from_model(self, db: Session, model: Base, item_id):
        """
        Get item from model by id
        :param db:
        :param item_id:
        :param model:
        :return:
        """
        return db.query(model).filter(model.id == item_id).first()

    def filter_by_item_ids(self, db: Session, model: Base, item_ids):
        """
        Filter expression to get items by list of ids
        :param db:
        :param model:
        :param item_ids:
        :return:
        """
        return db.query(model).filter(model.id.in_(item_ids)).all()

    def add(self, db: Session, model_obj: Base):
        """
        Add model object
        :param db:
        :param model_obj:
        :return:
        """
        db.add(model_obj)
        db.commit()
        db.refresh(model_obj)
        return model_obj

    def create_product(self, db: Session, product: ProductCreate):
        """
        Add new product
        :param db:
        :param product:
        :return: dict
        """
        product = Product(**product.dict())
        return self.add(db, product)

    def create_order(self, db: Session, order_data: OrderCreate, products: Dict):
        """
        Create order
        :param db:
        :param order_data:
        :return: order obj
        """
        try:
            total_price = 0.0
            order_items = []

            for item in order_data.products:
                product = products[item.product_id]

                # Calculate total price
                total_price += product.price * item.quantity
                product.stock -= item.quantity  # Deduct stock

            # Step 1: Create Order
            order_obj = Order(total_price=total_price, status="placed")  # Remove `products` argument
            order = self.add(db, order_obj)

            # Step 2: Create Order Items
            for item in order_data.products:
                order_items.append(OrderItem(order_id=order.id, product_id=item.product_id, quantity=item.quantity))

            db.bulk_save_objects(order_items)
            db.commit()
            db.refresh(order)

            return order

        except SQLAlchemyError as e:
            db.rollback()
            traceback.print_exc()
            raise CustomHTTPException(status_code=500, detail="An error occurred while processing the order",
                                      errors=str(e))
