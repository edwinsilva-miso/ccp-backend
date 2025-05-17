import uuid

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..database.declarative_base import Base


class ClientInfoModel(Base):
    """
    Client model for SQLAlchemy.
    """
    __tablename__ = 'client_info'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    order_id = Column(String, ForeignKey('orders.id'), unique=True, nullable=False)

    # Relationships
    # One-to-one relationship with Order
    order = relationship("OrderModel", back_populates="client_info")
