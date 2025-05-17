"""
Declarative base for SQLAlchemy models.
"""

import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Check if we're running tests
is_test = 'pytest' in sys.modules

if is_test:
    # Use SQLite in-memory database for tests
    db_path = 'sqlite:///:memory:'
else:
    # Use environment variables for production
    db_user = os.environ.get('DB_USER')
    db_password = os.environ.get('DB_PASSWORD')
    db_host = os.environ.get('DB_HOST')
    db_port = os.environ.get('DB_PORT')
    db_name = os.environ.get('DB_NAME')

    db_path = os.environ.get('DATABASE_URL')
    if not db_path:
        # Make sure none of the components are 'None' string
        if db_port == 'None':
            db_port = None

        # Validate that we have all required parameters
        if not all([db_user, db_password, db_host, db_port, db_name]):
            raise ValueError("Missing database connection parameters")

        db_path = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

engine = create_engine(db_path)
Session = sessionmaker(bind=engine)

Base = declarative_base()


def open_session():
    """
    Opens a new session for database operations.
    :return: A new SQLAlchemy session.
    """
    return Session()
