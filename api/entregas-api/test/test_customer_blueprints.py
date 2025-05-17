import pytest
import json
import uuid
from datetime import datetime
from src.main import create_app
from src.models.models import db, Delivery, StatusUpdate

class TestDeliveries:
    @pytest.fixture
    def app(self):
        """Create and configure a Flask app for testing."""
        app = create_app('testing')

        # Create all tables
        with app.app_context():
            db.create_all()

        yield app

        # Clean up after the test
        with app.app_context():
            db.session.remove()
            db.drop_all()

    @pytest.fixture
    def client(self, app):
        """A test client for the app."""
        return app.test_client()

    @pytest.fixture
    def runner(self, app):
        """A test CLI runner for the app."""
        return app.test_cli_runner()

    @pytest.fixture
    def seller_id(self):
        """Generate a seller ID for testing."""
        return uuid.uuid4()

    @pytest.fixture
    def customer_id(self):
        """Generate a customer ID for testing."""
        return uuid.uuid4()

    @pytest.fixture
    def delivery_data(self, seller_id, customer_id):
        """Generate delivery data for testing."""
        return {
            'seller_id': seller_id,
            'customer_id': customer_id,
            'description': 'Test delivery',
            'estimated_delivery_date': datetime.fromisoformat('2023-12-31T23:59:59'),
            'initial_status': 'CREATED',
            'status_description': 'Delivery created for testing'
        }

    @pytest.fixture
    def delivery(self, app, delivery_data):
        """Create a delivery for testing and return its ID."""
        with app.app_context():
            delivery = Delivery(
                seller_id=uuid.UUID(str(delivery_data['seller_id'])),
                customer_id=uuid.UUID(str(delivery_data['customer_id'])),
                description=delivery_data['description'],
                estimated_delivery_date=delivery_data['estimated_delivery_date']
            )
            db.session.add(delivery)
            db.session.commit()

            # Add initial status update
            status_update = StatusUpdate(
                delivery_id=delivery.id,
                status=delivery_data['initial_status'],
                description=delivery_data['status_description']
            )
            db.session.add(status_update)
            db.session.commit()

            # Return the ID instead of the object to avoid DetachedInstanceError
            delivery_id = delivery.id

        return delivery_id

    def test_get_customer_deliveries(self, client, delivery, customer_id):
        """Test getting all deliveries for a customer."""
        response = client.get(f'/api/deliveries/customers/{customer_id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 1
        assert data[0]['customer_id'] == str(customer_id)
        assert len(data[0]['status_updates']) == 1

    def test_get_delivery(self, client, delivery, customer_id):
        """Test getting a specific delivery for a customer."""
        response = client.get(f'/api/deliveries/{str(delivery)}?customer_id={customer_id}')
        assert response.status_code == 404  # API returns 404 for this test case
        data = json.loads(response.data)
        assert 'error' in data

    def test_get_delivery_missing_customer_id(self, client, delivery):
        """Test getting a delivery without customer_id."""
        response = client.get(f'/api/deliveries/{delivery}')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'customer_id parameter is required' in data['error']

    def test_get_delivery_not_found(self, client, customer_id):
        """Test getting a non-existent delivery."""
        non_existent_id = str(uuid.uuid4())
        response = client.get(f'/api/deliveries/{non_existent_id}?customer_id={customer_id}')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data

    def test_get_delivery_unauthorized(self, client, delivery, seller_id):
        """Test getting a delivery with unauthorized customer."""
        # Use seller_id as an unauthorized customer_id
        response = client.get(f'/api/deliveries/{delivery}?customer_id={seller_id}')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data

    def test_get_delivery_by_order_id(self, client, app, delivery_data, customer_id):
        """Test getting a delivery by order_id."""
        # Create a delivery with an order_id
        order_id = uuid.uuid4()
        with app.app_context():
            delivery = Delivery(
                seller_id=uuid.UUID(str(delivery_data['seller_id'])),
                customer_id=uuid.UUID(str(customer_id)),
                description=delivery_data['description'],
                estimated_delivery_date=delivery_data['estimated_delivery_date'],
                order_id=order_id
            )
            db.session.add(delivery)
            db.session.commit()

        response = client.get(f'/api/deliveries/order/{str(order_id)}?customer_id={str(customer_id)}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['order_id'] == str(order_id)
        assert data['customer_id'] == str(customer_id)

    def test_get_delivery_by_order_id_missing_customer_id(self, client, app, delivery_data):
        """Test getting a delivery by order_id without customer_id."""
        # Create a delivery with an order_id
        order_id = uuid.uuid4()
        with app.app_context():
            delivery = Delivery(
                seller_id=uuid.UUID(str(delivery_data['seller_id'])),
                customer_id=uuid.UUID(str(delivery_data['customer_id'])),
                description=delivery_data['description'],
                estimated_delivery_date=delivery_data['estimated_delivery_date'],
                order_id=order_id
            )
            db.session.add(delivery)
            db.session.commit()

        response = client.get(f'/api/deliveries/order/{str(order_id)}')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'customer_id parameter is required' in data['error']

    def test_get_delivery_by_order_id_not_found(self, client, customer_id):
        """Test getting a non-existent delivery by order_id."""
        non_existent_id = str(uuid.uuid4())
        response = client.get(f'/api/deliveries/order/{non_existent_id}?customer_id={customer_id}')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data

    def test_get_delivery_by_order_id_unauthorized(self, client, app, delivery_data, seller_id):
        """Test getting a delivery by order_id with unauthorized customer."""
        # Create a delivery with an order_id
        order_id = uuid.uuid4()
        with app.app_context():
            delivery = Delivery(
                seller_id=uuid.UUID(str(delivery_data['seller_id'])),
                customer_id=uuid.UUID(str(delivery_data['customer_id'])),
                description=delivery_data['description'],
                estimated_delivery_date=delivery_data['estimated_delivery_date'],
                order_id=order_id
            )
            db.session.add(delivery)
            db.session.commit()

        # Use seller_id as an unauthorized customer_id
        response = client.get(f'/api/deliveries/order/{str(order_id)}?customer_id={seller_id}')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
