import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Float
from sqlalchemy.dialects.postgresql import UUID

from ..database.declarative_base import Base


class SellingPlanModel(Base):
    """
    SellingPlan model for SQLAlchemy.
    """

    __tablename__ = 'selling_plan'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=False)
    target_amount = Column(Float, nullable=True)
    target_date = Column(String(50), nullable=True)
    status = Column(String(20), nullable=False, default="active")
    created_at = Column(DateTime, nullable=True, default=datetime.utcnow)