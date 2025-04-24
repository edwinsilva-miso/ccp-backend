import enum
from datetime import datetime

import sqlalchemy
from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from ..database.declarative_base import Base

class PaymentStatusEnum(enum.Enum):
    CANCELADO = 'CANCELADO'
    APROBADO = 'APROBADO'
    RECHAZADO = 'RECHAZADO'

class PaymentMethodEnum(enum.Enum):
    TARJETA_CREDITO = 'TARJETA DE CREDITO'


class PaymentModel(Base):
    """
    Payment model for SQLAlchemy.
    """
    __tablename__ = 'payments'

    id = Column(String, primary_key=True, nullable=False)
    order_id = Column(String, ForeignKey('orders.id'), unique=True, nullable=False)
    amount = Column(Float, nullable=False)
    card_number = Column(String, nullable=True)
    cvv = Column(String, nullable=True)
    expiry_date = Column(String, nullable=True)
    currency = Column(String, nullable=False)
    payment_method = Column(sqlalchemy.Enum(PaymentMethodEnum), default=PaymentMethodEnum.TARJETA_CREDITO)
    transaction_id = Column(String, nullable=True)
    status = Column(sqlalchemy.Enum(PaymentStatusEnum), default=PaymentStatusEnum.APROBADO)
    transaction_date = Column(DateTime, nullable=False)


    # Relationships
    order = relationship("OrderModel", back_populates="payments")