import enum
import uuid

from datetime import datetime

import sqlalchemy
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID

from ..database.declarative_base import Base


class StatusEnum(enum.Enum):
    ACTIVO = 'ACTIVO'
    INACTIVO = 'INACTIVO'


class ProviderModel(Base):
    """
    Provider model for SQLAlchemy.
    """
    __tablename__ = 'providers'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nit = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    legal_representative = Column(String, nullable=False)
    country = Column(String, nullable=False)
    status = Column(sqlalchemy.Enum(StatusEnum), default=StatusEnum.ACTIVO)
    createdAt = Column(DateTime, nullable=True, default=datetime.utcnow())
    updatedAt = Column(DateTime, nullable=True)
