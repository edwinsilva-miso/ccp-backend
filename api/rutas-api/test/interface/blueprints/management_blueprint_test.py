import pytest
from sqlalchemy.orm import sessionmaker, declarative_base
from src.main import create_app
from test.conftest import TestConfig

Base = declarative_base()


class TestManagementBlueprint:
    @pytest.fixture(scope="function")
    def client(self):
        app = create_app(config_class=TestConfig)

        with app.test_client() as client:
            yield client


    def test_health_check(self, client):
        response = client.get('/health')
        data = response.get_json()

        assert response.status_code == 200
        assert data['status'] == 'healthy'
