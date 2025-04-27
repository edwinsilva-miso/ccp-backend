import os
from uuid import uuid4

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers, declarative_base

Base = declarative_base()

os.environ["DATABASE_URL"] = "sqlite:///:memory:"


class TestConfig:
    # Flask config
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    DEBUG = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 't')

    # OpenRoute Service config
    OPENROUTE_API_KEY = os.environ.get('OPENROUTE_API_KEY', '')
    OPENROUTE_BASE_URL = os.environ.get('OPENROUTE_BASE_URL', 'https://api.openrouteservice.org')

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("sqlite:///:memory:")

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        yield session
    finally:
        session.close()
        engine.dispose()


@pytest.fixture
def app():
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"
    os.environ["ENVIRONMENT"] = "test"

    from src.main import create_app
    app = create_app(config_class=TestConfig)

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def sample_route_data():
    return {
        "id": uuid4(),
        "name": "Sample Route",
        "description": "some description",
        "waypoints": [
            {
                "id": uuid4(),
                "latitude": 40.7128,
                "longitude": -74.0060,
                "name": None,
                "address": None,
                "order": 0
            }
        ]
    }

"""
    waypoints = [
        Waypoint(
            id=uuid4(),
            latitude=40.7128,
            longitude=-74.0060,
            name=None,
            address=None,
            order=0,
            created_at=datetime.utcnow()
        ),
        Waypoint(
            id=uuid4(),
            latitude=34.0522,
            longitude=-118.2437,
            name="Los Angeles",
            address="California, USA",
            order=1,
            created_at=datetime.utcnow()
        )
    ]

    route = Route(
        id=uuid4(),
        name="Cross-country Route",
        waypoints=waypoints,
        description="A test route spanning two cities.",
        user_id=None,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    return route
"""