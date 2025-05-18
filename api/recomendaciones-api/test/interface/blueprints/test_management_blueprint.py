import pytest

from src.main import create_app


class TestManagementBlueprint:
    @pytest.fixture
    def client(self):
        app = create_app()
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client

    def test_health_check(self, client):
        response = client.get('/health')
        data = response.get_json()

        assert response.status_code == 200
        assert data['status'] == 'UP'
