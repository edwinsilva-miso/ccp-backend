import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..database.declarative_base import Base


class OrderHistoryModel(Base):
    """
    Order History model for SQLAlchemy.
    """
    __tablename__ = 'order_history'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(String, ForeignKey('orders.id'), nullable=False)
    status = Column(String, nullable=False)
    description = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.utcnow())

    # Relationships
    orders = relationship("OrderModel", back_populates="order_history", foreign_keys=[order_id])
