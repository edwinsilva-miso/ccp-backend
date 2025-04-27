from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from ..database.declarative_base import Base


class OrderItemsModel(Base):
    """
    Order Item model for SQLAlchemy.
    """
    __tablename__ = 'order_items'

    id = Column(String, primary_key=True, nullable=False)
    order_id = Column(String, ForeignKey('orders.id'), nullable=False)
    product_id = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    currency = Column(String, nullable=False)

    # Relationships - simplified to remove the problematic cascade
    orders = relationship("OrderModel", back_populates="order_items")