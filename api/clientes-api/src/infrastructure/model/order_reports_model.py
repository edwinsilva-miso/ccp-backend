import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID

from ..database.declarative_base import Base


class OrderReportsModel(Base):
    """
    OrderReportsModel is a SQLAlchemy model that represents the order reports in the database.
    """
    __tablename__ = 'order_reports'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    name = Column(String, nullable=False)
    date = Column(DateTime, nullable=True, default=datetime.utcnow())
    url = Column(String, nullable=False)
