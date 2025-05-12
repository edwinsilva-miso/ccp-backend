import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID

from ..database.declarative_base import Base


class ClientVisitRecordModel(Base):
    """
    SQLAlchemy model for the Client Visit Record entity.
    This class defines the structure of the client visit record table in the database.
    """
    __tablename__ = 'client_visit_records'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_id = Column(UUID(as_uuid=True), nullable=False)
    salesman_id = Column(UUID(as_uuid=True), nullable=False)
    visit_date = Column(DateTime, nullable=True, default=datetime.utcnow)
    notes = Column(String(255), nullable=True)
