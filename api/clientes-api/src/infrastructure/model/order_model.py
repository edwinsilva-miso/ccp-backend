import enum
from datetime import datetime

import sqlalchemy
from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.orm import relationship

from ..database.declarative_base import Base


class OrderStatusEnum(enum.Enum):
    PENDIENTE = 'PENDIENTE'
    EN_PROCESO = 'EN PROCESO'
    COMPLETADO = 'COMPLETADO'
    CANCELADO = 'CANCELADO'
    FALLIDO = 'FALLIDO'


class OrderModel(Base):
    """
    Order model for SQLAlchemy.
    """
    __tablename__ = 'orders'

    id = Column(String, primary_key=True, nullable=False)
    client_id = Column(String, nullable=False)
    quantity = Column(String, nullable=False)
    subtotal = Column(Float, nullable=False)
    tax = Column(Float, nullable=False)
    total = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    status = Column(sqlalchemy.Enum(OrderStatusEnum), default=OrderStatusEnum.PENDIENTE)
    created_at = Column(DateTime, nullable=True, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=True)

    # Relationships
    client_info = relationship("ClientInfoModel", uselist=False, back_populates="order", cascade="all, delete-orphan")
    order_details = relationship("OrderDetailsModel", back_populates="orders", cascade="all, delete-orphan")
    payment = relationship("PaymentModel", uselist=False, back_populates="order", cascade="all, delete-orphan")
