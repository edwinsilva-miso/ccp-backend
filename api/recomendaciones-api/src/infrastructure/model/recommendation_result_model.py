import uuid
from datetime import datetime

from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID

from ..database.declarative_base import Base


class RecommendationResultModel(Base):
    """
    Recommendation result model for SQLAlchemy.
    """
    __tablename__ = 'recommendation_results'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(String, nullable=False)
    events = Column(String, nullable=False)
    target_sales_amount = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    recommendation = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=True, default=datetime.utcnow())
