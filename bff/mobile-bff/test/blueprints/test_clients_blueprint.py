import pytest
from unittest.mock import patch, Mock
import json
from src.blueprints.clients_blueprint import orders_blueprint


@pytest.fixture
def client():
    from flask import Flask
    app = Flask(__name__)
    app.register_blueprint(orders_blueprint)
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_order_data():
    return {
        "clientId": "123e4567-e89b-12d3-a456-426614174000",
        "items": [
            {
                "productId": "123e4567-e89b-12d3-a456-426614174001",
                "quantity": 2
            }
        ],
        "totalPrice": 200.0,
        "shippingAddress": "123 Main St"
    }


@pytest.fixture
def mock_order_response():
    return {
        "id": "123e4567-e89b-12d3-a456-426614174002",
        "clientId": "123e4567-e89b-12d3-a456-426614174000",
        "orderDetails": [
            {
                "productId": "123e4567-e89b-12d3-a456-426614174001",
                "quantity": 2
            }
        ],
        "totalPrice": 200.0,
        "shippingAddress": "123 Main St",
        "status": "CREATED",
        "createdAt": "2023-01-01T00:00:00Z"
    }


def test_create_order_success(client, mock_order_data, mock_order_response):
    with patch('src.blueprints.clients_blueprint.ClientsAdapter') as MockAdapter:
        mock_instance = MockAdapter.return_value
        mock_instance.create_order.return_value = json.dumps(mock_order_response), 201

        response = client.post(
            '/bff/v1/mobile/clients/orders/',
            headers={'Authorization': 'Bearer fake_token'},
            json=mock_order_data
        )

        data = json.loads(response.data)
        assert response.status_code == 201
        assert data == mock_order_response
        MockAdapter.assert_called_once()
        mock_instance.create_order.assert_called_once_with('fake_token', mock_order_data)


def test_create_order_missing_token(client, mock_order_data):
    response = client.post(
        '/bff/v1/mobile/clients/orders/',
        json=mock_order_data
    )

    data = json.loads(response.data)
    assert response.status_code == 401
    assert data['msg'] == 'Unauthorized'


def test_list_orders_success(client):
    mock_orders = [
        {
            "id": "123e4567-e89b-12d3-a456-426614174002",
            "clientId": "123e4567-e89b-12d3-a456-426614174000",
            "status": "DELIVERED"
        },
        {
            "id": "123e4567-e89b-12d3-a456-426614174003",
            "clientId": "123e4567-e89b-12d3-a456-426614174000",
            "status": "CREATED"
        }
    ]

    with patch('src.blueprints.clients_blueprint.ClientsAdapter') as MockAdapter:
        mock_instance = MockAdapter.return_value
        mock_instance.lists_orders.return_value = json.dumps(mock_orders), 200

        response = client.get(
            '/bff/v1/mobile/clients/orders/?clientId=123e4567-e89b-12d3-a456-426614174000',
            headers={'Authorization': 'Bearer fake_token'}
        )

        data = json.loads(response.data)
        assert response.status_code == 200
        assert data == mock_orders
        MockAdapter.assert_called_once()
        mock_instance.lists_orders.assert_called_once_with(
            'fake_token',
            '123e4567-e89b-12d3-a456-426614174000'
        )


def test_list_orders_missing_token(client):
    response = client.get('/bff/v1/mobile/clients/orders/?clientId=123')

    data = json.loads(response.data)
    assert response.status_code == 401
    assert data['msg'] == 'Unauthorized'


def test_get_order_success(client, mock_order_response):
    with patch('src.blueprints.clients_blueprint.ClientsAdapter') as MockAdapter:
        mock_instance = MockAdapter.return_value
        mock_instance.get_order_by_id.return_value = json.dumps(mock_order_response), 200

        order_id = '123e4567-e89b-12d3-a456-426614174002'
        response = client.get(
            f'/bff/v1/mobile/clients/orders/{order_id}',
            headers={'Authorization': 'Bearer fake_token'}
        )

        data = json.loads(response.data)
        assert response.status_code == 200
        assert data == mock_order_response
        MockAdapter.assert_called_once()
        mock_instance.get_order_by_id.assert_called_once_with('fake_token', order_id)


def test_get_order_missing_token(client):
    order_id = '123e4567-e89b-12d3-a456-426614174002'
    response = client.get(f'/bff/v1/mobile/clients/orders/{order_id}')

    data = json.loads(response.data)
    assert response.status_code == 401
    assert data['msg'] == 'Unauthorized'