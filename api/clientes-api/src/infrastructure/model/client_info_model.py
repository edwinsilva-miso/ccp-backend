from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from ..database.declarative_base import Base


class ClientInfoModel(Base):
    """
    Client model for SQLAlchemy.
    """
    __tablename__ = 'client_info'

    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    order_id = Column(String, ForeignKey('orders.id'), unique=True, nullable=False)

    # Relationships
    # One-to-one relationship with Order
    order = relationship("OrderModel", back_populates="client_info")
