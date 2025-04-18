import uuid
from datetime import datetime

import sqlalchemy
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSON

from ..database.declarative_base import Base


class ProductModel(Base):
    """
    Product model for SQLAlchemy.
    """
    __tablename__ = 'products'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    description = Column(String, nullable=False)
    details = Column(String, nullable=False)
    storage_conditions = Column(JSON, nullable=False)
    price = Column(sqlalchemy.Float, nullable=False)
    currency = Column(String, nullable=False)
    delivery_time = Column(sqlalchemy.Integer, nullable=False)
    manufacturer_id = Column(UUID(as_uuid=True), nullable=False)
    images = Column(JSON, nullable=False)
    createdAt = Column(DateTime, nullable=True, default=datetime.utcnow())
    updatedAt = Column(DateTime, nullable=True)
