from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from ..database.declarative_base import Base


class OrderDetailsModel(Base):
    """
    Order details model for SQLAlchemy.
    """
    __tablename__ = 'order_details'

    id = Column(String, primary_key=True, nullable=False)
    order_id = Column(String, ForeignKey('orders.id'), nullable=False)
    product_id = Column(String, nullable=False)
    quantity = Column(Float, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    currency = Column(String, nullable=False)

    # Relationships
    order = relationship("OrderModel", back_populates="order_details")
