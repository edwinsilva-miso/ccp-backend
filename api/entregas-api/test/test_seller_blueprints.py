import unittest
import json
import uuid
from datetime import datetime
from src.main import create_app
from src.models.models import db, Delivery, StatusUpdate

class TestSellerBlueprints(unittest.TestCase):
    def setUp(self):
        """Create and configure a Flask app for testing."""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        # Default test UUIDs (these change for each test if needed)
        self.seller_id = str(uuid.uuid4())
        self.customer_id = str(uuid.uuid4())
        self.order_id = str(uuid.uuid4())

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def get_delivery_data(self):
        return {
            'seller_id': self.seller_id,
            'order_id': self.order_id,
            'customer_id': self.customer_id,
            'description': 'Test delivery',
            'estimated_delivery_date': datetime.fromisoformat('2023-12-31T23:59:59'),
            'initial_status': 'CREATED',
            'status_description': 'Delivery created for testing'
        }

    def create_delivery_in_db(self, delivery_data=None):
        """Helper to add a delivery and initial status to the DB."""
        if delivery_data is None:
            delivery_data = self.get_delivery_data()
        delivery = Delivery(
            seller_id=uuid.UUID(delivery_data['seller_id']),
            customer_id=uuid.UUID(delivery_data['customer_id']),
            description=delivery_data['description'],
            estimated_delivery_date=delivery_data['estimated_delivery_date']
        )
        db.session.add(delivery)
        db.session.commit()
        status_update = StatusUpdate(
            delivery_id=delivery.id,
            status=delivery_data['initial_status'],
            description=delivery_data['status_description']
        )
        db.session.add(status_update)
        db.session.commit()
        return delivery

    def test_create_delivery(self):
        delivery_data = self.get_delivery_data()
        request_data = {
            'order_id': delivery_data['order_id'],
            'customer_id': delivery_data['customer_id'],
            'seller_id': delivery_data['seller_id'],
            'description': delivery_data['description'],
            'estimated_delivery_date': delivery_data['estimated_delivery_date']
        }
        response = self.client.post('/api/seller/deliveries', json=request_data)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['seller_id'], delivery_data['seller_id'])
        self.assertEqual(data['customer_id'], delivery_data['customer_id'])
        self.assertEqual(data['description'], delivery_data['description'])

    def test_create_delivery_missing_field(self):
        delivery_data = self.get_delivery_data()
        delivery_data.pop('customer_id')
        # Note: This will actually fail due to 'estimated_delivery_date' not being serializable, handle accordingly
        # Remove any non-serializable
        delivery_data['estimated_delivery_date'] = delivery_data['estimated_delivery_date'].isoformat()
        response = self.client.post('/api/seller/deliveries', json=delivery_data)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertIn('Missing required field', data['error'])

    def test_get_seller_deliveries(self):
        self.create_delivery_in_db()
        response = self.client.get(f'/api/seller/deliveries?seller_id={self.seller_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['seller_id'], self.seller_id)
        self.assertEqual(len(data[0]['status_updates']), 1)

    def test_get_seller_deliveries_missing_seller_id(self):
        response = self.client.get('/api/seller/deliveries')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertIn('seller_id parameter is required', data['error'])

    def test_get_delivery(self):
        delivery = self.create_delivery_in_db()
        response = self.client.get(f'/api/seller/deliveries/{delivery.id}?seller_id={self.seller_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['id'], str(delivery.id))
        self.assertEqual(data['seller_id'], self.seller_id)

    def test_get_delivery_not_found(self):
        non_existent_id = str(uuid.uuid4())
        response = self.client.get(f'/api/seller/deliveries/{non_existent_id}?seller_id={self.seller_id}')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_get_delivery_unauthorized(self):
        delivery = self.create_delivery_in_db()
        response = self.client.get(f'/api/seller/deliveries/{delivery.id}?seller_id={self.customer_id}')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_update_delivery(self):
        delivery = self.create_delivery_in_db()
        update_data = {
            'seller_id': self.seller_id,
            'description': 'Updated description',
            'estimated_delivery_date': datetime.fromisoformat('2024-01-15T12:00:00')
        }
        response = self.client.put(f'/api/seller/deliveries/{delivery.id}', json=update_data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['description'], 'Updated description')

    def test_update_delivery_missing_seller_id(self):
        delivery = self.create_delivery_in_db()
        update_data = {'description': 'Updated description'}
        response = self.client.put(f'/api/seller/deliveries/{delivery.id}', json=update_data)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertIn('seller_id is required', data['error'])

    def test_delete_delivery(self):
        delivery = self.create_delivery_in_db()
        response = self.client.delete(f'/api/seller/deliveries/{delivery.id}?seller_id={self.seller_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Delivery deleted successfully')

    def test_delete_delivery_not_found(self):
        non_existent_id = str(uuid.uuid4())
        response = self.client.delete(f'/api/seller/deliveries/{non_existent_id}?seller_id={self.seller_id}')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_add_status_update(self):
        delivery = self.create_delivery_in_db()
        status_data = {
            'seller_id': self.seller_id,
            'status': 'SHIPPED',
            'description': 'Package has been shipped'
        }
        response = self.client.post(f'/api/seller/deliveries/{delivery.id}/status', json=status_data)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'SHIPPED')
        self.assertEqual(data['description'], 'Package has been shipped')

    def test_add_status_update_missing_status(self):
        delivery = self.create_delivery_in_db()
        status_data = {
            'seller_id': self.seller_id,
            'description': 'Package has been shipped'
        }
        response = self.client.post(f'/api/seller/deliveries/{delivery.id}/status', json=status_data)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertIn('Missing required field: status', data['error'])

    def test_update_status_update(self):
        delivery = self.create_delivery_in_db()
        status_update = StatusUpdate(
            delivery_id=delivery.id,
            status='PROCESSING',
            description='Processing the order'
        )
        db.session.add(status_update)
        db.session.commit()
        status_update_id = status_update.id

        update_data = {
            'seller_id': self.seller_id,
            'status': 'SHIPPED',
            'description': 'Package has been shipped'
        }
        response = self.client.put(f'/api/seller/status/{status_update_id}', json=update_data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'SHIPPED')
        self.assertEqual(data['description'], 'Package has been shipped')

    def test_delete_status_update(self):
        delivery = self.create_delivery_in_db()
        status_update = StatusUpdate(
            delivery_id=delivery.id,
            status='PROCESSING',
            description='Processing the order'
        )
        db.session.add(status_update)
        db.session.commit()
        status_update_id = status_update.id

        response = self.client.delete(f'/api/seller/status/{status_update_id}?seller_id={self.seller_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Status update deleted successfully')

if __name__ == '__main__':
    unittest.main()
