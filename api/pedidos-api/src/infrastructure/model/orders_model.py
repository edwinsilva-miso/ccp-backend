from datetime import datetime

from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.orm import relationship

from ..database.declarative_base import Base


class OrderModel(Base):
    """
    Order model for SQLAlchemy.
    """
    __tablename__ = 'orders'

    id = Column(String, primary_key=True, nullable=False)
    status = Column(String, nullable=False)
    subtotal = Column(Float, nullable=False)
    taxes = Column(Float, nullable=False)
    total = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    client_id = Column(String, nullable=False)
    order_date = Column(DateTime, default=datetime.utcnow())
    payment_id = Column(String, nullable=False)
    transaction_id = Column(String, nullable=False)
    transaction_status = Column(String, nullable=False)
    transaction_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=True, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=True)

    # Relationships
    order_items = relationship("OrderItemsModel", back_populates="orders", cascade="all, delete-orphan")
    order_history = relationship("OrderHistoryModel", back_populates="orders", cascade="all, delete-orphan")
