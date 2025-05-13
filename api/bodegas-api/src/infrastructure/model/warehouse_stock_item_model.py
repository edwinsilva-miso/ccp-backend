import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Float, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..database.declarative_base import Base


class WarehouseStockItemModel(Base):
    """
    Warehouse Stock Item model for SQLAlchemy.
    """

    __tablename__ = 'warehouse_stock_item'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    warehouse_id = Column(UUID(as_uuid=True), ForeignKey('warehouse.id'), nullable=False)
    item_id = Column(UUID(as_uuid=True), nullable=False)
    barcode = Column(String(255), nullable=True)
    identification_code = Column(String(255), nullable=True)
    width = Column(Float, nullable=True)
    height = Column(Float, nullable=True)
    depth = Column(Float, nullable=True)
    weight = Column(Float, nullable=True)
    hallway = Column(String(50), nullable=True)
    shelf = Column(String(50), nullable=True)
    sold = Column(Boolean, nullable=False, default=False)
    status = Column(String(20), nullable=False, default="active")
    created_at = Column(DateTime, nullable=True, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)

    # Relationship with warehouse
    warehouse = relationship("WarehouseModel", back_populates="stock_items")