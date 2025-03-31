import enum
import uuid
from datetime import datetime

import sqlalchemy
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID

from ..database.declarative_base import Base


class RoleEnum(enum.Enum):
    CLIENTE = 'CLIENTE'
    VENDEDOR = 'VENDEDOR'
    DIRECTIVO = 'DIRECTIVO'
    TRANSPORTISTA = 'TRANSPORTISTA'


class UserModel(Base):
    """
    User model for SQLAlchemy.
    """

    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    salt = Column(String)
    token = Column(String, nullable=True)
    role = Column(sqlalchemy.Enum(RoleEnum), default=RoleEnum.CLIENTE)
    is_active = Column(sqlalchemy.Boolean, default=True)
    expireAt = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=True, default=datetime.utcnow)
    updatedAt = Column(DateTime, nullable=True)
