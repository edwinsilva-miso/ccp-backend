import uuid

from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..database.declarative_base import Base


class OrderDetailsModel(Base):
    """
    Order details model for SQLAlchemy.
    """
    __tablename__ = 'order_details'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(String, ForeignKey('orders.id'), nullable=False)
    product_id = Column(String, nullable=False)
    quantity = Column(Float, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    currency = Column(String, nullable=False)

    # Relationships
    orders = relationship("OrderModel", back_populates="order_details")
