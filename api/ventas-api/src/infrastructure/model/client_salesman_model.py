import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID

from ..database.declarative_base import Base


class ClientSalesmanModel(Base):
    """
    ClientSalesman model for SQLAlchemy.
    """

    __tablename__ = 'client_salesman'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    salesman_id = Column(UUID(as_uuid=True), nullable=False)
    client_id = Column(UUID(as_uuid=True), nullable=False, unique=True)
    client_name = Column(String(255), nullable=False)
    client_phone = Column(String(20), nullable=False)
    client_email = Column(String(100), nullable=False)
    address = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)
    store_name = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=True, default=datetime.utcnow)
