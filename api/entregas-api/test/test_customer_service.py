import unittest
import uuid
from datetime import datetime
from src.main import create_app
from src.models.models import db, Delivery, StatusUpdate
from src.services.customer_service import CustomerService

class TestCustomerService(unittest.TestCase):

    def setUp(self):
        # Set up Flask test app and database
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        # Generate seller/customer IDs
        self.seller_id = str(uuid.uuid4())
        self.customer_id = str(uuid.uuid4())

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def get_delivery_data(self):
        return {
            'seller_id': self.seller_id,
            'customer_id': self.customer_id,
            'description': 'Test delivery',
            'estimated_delivery_date': datetime.fromisoformat('2023-12-31T23:59:59'),
            'initial_status': 'CREATED',
            'status_description': 'Delivery created for testing'
        }

    def create_delivery(self, delivery_data=None):
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

    def test_get_customer_deliveries(self):
        delivery = self.create_delivery()
        deliveries = CustomerService.get_customer_deliveries(uuid.UUID(self.customer_id))
        self.assertEqual(len(deliveries), 1)
        self.assertEqual(str(deliveries[0].customer_id), self.customer_id)

    def test_get_customer_deliveries_empty(self):
        different_customer_id = str(uuid.uuid4())
        deliveries = CustomerService.get_customer_deliveries(uuid.UUID(different_customer_id))
        self.assertEqual(len(deliveries), 0)

    def test_get_delivery(self):
        delivery = self.create_delivery()
        result = CustomerService.get_delivery(delivery.id, uuid.UUID(self.customer_id))
        self.assertIsNotNone(result)
        self.assertEqual(result.id, delivery.id)
        self.assertEqual(str(result.customer_id), self.customer_id)

    def test_get_delivery_not_found(self):
        non_existent_id = uuid.uuid4()
        result = CustomerService.get_delivery(non_existent_id, uuid.UUID(self.customer_id))
        self.assertIsNone(result)

    def test_get_delivery_unauthorized(self):
        delivery = self.create_delivery()
        # Use seller_id as unauthorized customer_id
        result = CustomerService.get_delivery(delivery.id, uuid.UUID(self.seller_id))
        self.assertIsNone(result)

    def test_get_delivery_by_order_id(self):
        delivery_data = self.get_delivery_data()
        order_id = uuid.uuid4()
        delivery = Delivery(
            seller_id=uuid.UUID(delivery_data['seller_id']),
            customer_id=uuid.UUID(self.customer_id),
            description=delivery_data['description'],
            order_id=order_id
        )
        db.session.add(delivery)
        db.session.commit()
        result = CustomerService.get_delivery_by_order_id(order_id, uuid.UUID(self.customer_id))
        self.assertIsNotNone(result)
        self.assertEqual(result.order_id, order_id)
        self.assertEqual(str(result.customer_id), self.customer_id)

    def test_get_delivery_by_order_id_not_found(self):
        non_existent_id = uuid.uuid4()
        result = CustomerService.get_delivery_by_order_id(non_existent_id, uuid.UUID(self.customer_id))
        self.assertIsNone(result)

    def test_get_delivery_by_order_id_unauthorized(self):
        delivery_data = self.get_delivery_data()
        order_id = uuid.uuid4()
        # Regular delivery with delivery_data
        delivery = Delivery(
            seller_id=uuid.UUID(delivery_data['seller_id']),
            customer_id=uuid.UUID(delivery_data['customer_id']),
            description=delivery_data['description'],
            order_id=order_id
        )
        db.session.add(delivery)
        db.session.commit()
        result = CustomerService.get_delivery_by_order_id(order_id, uuid.UUID(self.seller_id))
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()