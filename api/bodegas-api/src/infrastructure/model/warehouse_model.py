import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..database.declarative_base import Base


class WarehouseModel(Base):
    """
    Warehouse model for SQLAlchemy.
    """

    __tablename__ = 'warehouse'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    location = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=False)
    name = Column(String(255), nullable=False)
    administrator_id = Column(UUID(as_uuid=True), nullable=False)
    status = Column(String(20), nullable=False, default="active")
    created_at = Column(DateTime, nullable=True, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)

    # Relationship with stock items
    stock_items = relationship("WarehouseStockItemModel", back_populates="warehouse")
