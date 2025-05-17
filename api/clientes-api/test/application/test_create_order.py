import unittest
from unittest.mock import Mock, patch, ANY
import uuid
from datetime import datetime

from src.application.create_order import CreateOrder
from src.domain.entities.order_dto import OrderDTO
from src.domain.entities.payment_dto import PaymentDTO
from src.domain.entities.client_info_dto import ClientInfoDTO
from src.domain.entities.order_details_dto import OrderDetailsDTO


class TestCreateOrder(unittest.TestCase):
    def setUp(self):
        self.order_repository = Mock()
        self.payments_port = Mock()
        self.messaging_port = Mock()

        self.create_order = CreateOrder(
            order_repository=self.order_repository,
            payments_port=self.payments_port,
            messaging_port=self.messaging_port
        )

        # Sample order data
        self.order_data = {
            'clientId': 'client123',
            'quantity': 2,
            'subtotal': 100.0,
            'tax': 19.0,
            'total': 119.0,
            'currency': 'USD',
            'payment': {
                'amount': 119.0,
                'cardNumber': '4111111111111111',
                'cvv': '123',
                'expiryDate': '12/25',
                'currency': 'USD'
            },
            'clientInfo': {
                'name': 'John Doe',
                'address': '123 Main St',
                'phone': '123456789',
                'email': 'john@example.com'
            },
            'orderDetails': [
                {
                    'productId': 'product123',
                    'quantity': 1,
                    'unitPrice': 50.0,
                    'totalPrice': 50.0,
                    'currency': 'USD'
                },
                {
                    'productId': 'product456',
                    'quantity': 1,
                    'unitPrice': 50.0,
                    'totalPrice': 50.0,
                    'currency': 'USD'
                }
            ]
        }

        # Mock payment response
        self.payment_response = {
            'id': str(uuid.uuid4()),
            'transactionReference': 'tx123456',
            'status': 'APROBADO',
            'cardNumber': '4111111111111111',
            'timestamp': datetime.now().isoformat()
        }

        # Setup payment port to return success
        self.payments_port.process_payment.return_value = self.payment_response

        # Setup order repository to return an order
        self.mock_order = Mock(spec=OrderDTO)
        self.mock_order.id = str(uuid.uuid4())
        self.mock_order.status = 'COMPLETADO'
        self.mock_order.to_dict.return_value = {
            'id': self.mock_order.id,
            'status': 'COMPLETADO',
            'clientId': 'client123',
            'payment': {
                'id': self.payment_response['id'],
                'status': 'APROBADO',
                'transactionId': 'tx123456',
                'transactionDate': self.payment_response['timestamp']
            },
            'orderDetails': [
                {'id': str(uuid.uuid4()), 'productId': 'product123', 'quantity': 1, 'unitPrice': 50.0,
                 'totalPrice': 50.0, 'currency': 'USD'},
                {'id': str(uuid.uuid4()), 'productId': 'product456', 'quantity': 1, 'unitPrice': 50.0,
                 'totalPrice': 50.0, 'currency': 'USD'}
            ],
            'subtotal': 100.0,
            'tax': 19.0,
            'total': 119.0,
            'currency': 'USD',
            'createdAt': datetime.now().isoformat()
        }

        # Add the order_details attribute - this is what was missing
        order_details = [
            Mock(spec=OrderDetailsDTO) for _ in range(2)
        ]
        for i, detail in enumerate(order_details):
            detail.product_id = f'product{i + 1}'
            detail.quantity = 1

        self.mock_order.order_details = order_details

        self.order_repository.add.return_value = self.mock_order

    @patch('uuid.uuid4')
    @patch('src.application.create_order.validate')
    def test_execute_successful_order(self, mock_validate, mock_uuid):
        # Setup
        mock_uuid.side_effect = [uuid.UUID('12345678-1234-5678-1234-567812345678')] * 10

        # Execute
        result, status_code = self.create_order.execute(self.order_data, 'salesman123')

        # Verify
        mock_validate.assert_called_once_with(self.order_data)
        self.payments_port.process_payment.assert_called_once()
        self.order_repository.add.assert_called_once()

        # Check messaging was called twice (stock update and order production)
        self.assertEqual(self.messaging_port.send_message.call_count, 2)

        # Verify the exchange and routing keys
        stock_call, order_call = self.messaging_port.send_message.call_args_list
        self.assertEqual(stock_call[1]['exchange'], 'update_stock_exchange')
        self.assertEqual(stock_call[1]['routing_key'], 'update_stock_routing_key')
        self.assertEqual(order_call[1]['exchange'], 'order_initiated_exchange')
        self.assertEqual(order_call[1]['routing_key'], 'order_initiated_routing_key')

        # Check the status code
        self.assertEqual(status_code, 201)

        # Verify result is the order dict
        self.assertEqual(result, self.mock_order.to_dict())

    @patch('uuid.uuid4')
    @patch('src.application.create_order.validate')
    def test_execute_failed_payment(self, mock_validate, mock_uuid):
        # Setup
        mock_uuid.side_effect = [uuid.UUID('12345678-1234-5678-1234-567812345678')] * 10

        # Make payment fail
        failed_payment = dict(self.payment_response)
        failed_payment['status'] = 'RECHAZADO'
        self.payments_port.process_payment.return_value = failed_payment

        # Make order status reflect payment failure
        self.mock_order.status = 'FALLIDO'

        # Execute
        result, status_code = self.create_order.execute(self.order_data, 'salesman123')

        # Verify
        mock_validate.assert_called_once_with(self.order_data)
        self.payments_port.process_payment.assert_called_once()
        self.order_repository.add.assert_called_once()

        # Check no messages were sent (should not update stock or produce order)
        self.messaging_port.send_message.assert_not_called()

        # Check the status code indicates payment required
        self.assertEqual(status_code, 402)

    @patch('uuid.uuid4')
    @patch('src.application.create_order.validate')
    def test_execute_without_salesman(self, mock_validate, mock_uuid):
        # Setup
        mock_uuid.side_effect = [uuid.UUID('12345678-1234-5678-1234-567812345678')] * 10

        # Create a new OrderDTO mock with proper order_details attribute
        order_dto = Mock(spec=OrderDTO)
        order_dto.id = str(uuid.uuid4())
        order_dto.status = 'COMPLETADO'
        order_dto.to_dict.return_value = self.mock_order.to_dict()

        # Add order details to the order_dto
        order_details = [
            Mock(spec=OrderDetailsDTO) for _ in range(2)
        ]
        for i, detail in enumerate(order_details):
            detail.product_id = f'product{i + 1}'
            detail.quantity = 1

        order_dto.order_details = order_details

        # Use this improved mock for this test
        self.order_repository.add.return_value = order_dto

        # Execute
        result, status_code = self.create_order.execute(self.order_data, None)

        # Verify
        mock_validate.assert_called_once_with(self.order_data)
        self.payments_port.process_payment.assert_called_once()
        self.order_repository.add.assert_called_once()

        # Verify the order was created with salesman_id=None
        called_dto = self.order_repository.add.call_args[0][0]
        self.assertIsNone(called_dto.salesman_id)

        # Verify both messaging calls were made (stock update and order production)
        self.assertEqual(self.messaging_port.send_message.call_count, 2)

    @patch('uuid.uuid4')
    @patch('src.application.create_order.validate')
    def test_payment_processing_error(self, mock_validate, mock_uuid):
        # Setup
        mock_uuid.side_effect = [uuid.UUID('12345678-1234-5678-1234-567812345678')] * 10

        # Make payment processing return None (error case)
        self.payments_port.process_payment.return_value = None

        # Execute with expectation of error
        with self.assertRaises(AttributeError):  # Assuming None payment causes an AttributeError
            self.create_order.execute(self.order_data, 'salesman123')

    def test_update_products_stock(self):
        # Setup
        order_details = [
            OrderDetailsDTO(
                id=str(uuid.uuid4()),
                order_id=str(uuid.uuid4()),
                product_id='product123',
                quantity=3,
                unit_price=10.0,
                total_price=30.0,
                currency='USD'
            ),
            OrderDetailsDTO(
                id=str(uuid.uuid4()),
                order_id=str(uuid.uuid4()),
                product_id='product456',
                quantity=1,
                unit_price=20.0,
                total_price=20.0,
                currency='USD'
            )
        ]

        # Execute
        self.create_order._update_products_stock(order_details)

        # Verify
        self.messaging_port.send_message.assert_called_once()
        kwargs = self.messaging_port.send_message.call_args[1]

        # Check exchange and routing key
        self.assertEqual(kwargs['exchange'], 'update_stock_exchange')
        self.assertEqual(kwargs['routing_key'], 'update_stock_routing_key')

        # Check message content
        message = kwargs['message']
        self.assertEqual(len(message['products']), 2)
        self.assertEqual(message['products'][0]['productId'], 'product123')
        self.assertEqual(message['products'][0]['quantity'], 3)
        self.assertEqual(message['products'][1]['productId'], 'product456')
        self.assertEqual(message['products'][1]['quantity'], 1)

    def test_produce_order(self):
        # Setup
        order_info = {
            'id': str(uuid.uuid4()),
            'createdAt': datetime.now().isoformat(),
            'subtotal': 100.0,
            'tax': 19.0,
            'total': 119.0,
            'currency': 'USD',
            'clientId': 'client123',
            'payment': {
                'id': str(uuid.uuid4()),
                'status': 'APROBADO',
                'transactionId': 'tx123456',
                'transactionDate': datetime.now().isoformat()
            },
            'orderDetails': [
                {'id': str(uuid.uuid4()), 'productId': 'product123', 'quantity': 1, 'unitPrice': 50.0,
                 'totalPrice': 50.0, 'currency': 'USD'},
                {'id': str(uuid.uuid4()), 'productId': 'product456', 'quantity': 1, 'unitPrice': 50.0,
                 'totalPrice': 50.0, 'currency': 'USD'}
            ]
        }

        # Execute
        self.create_order._produce_order(order_info)

        # Verify
        self.messaging_port.send_message.assert_called_once()
        kwargs = self.messaging_port.send_message.call_args[1]

        # Check exchange and routing key
        self.assertEqual(kwargs['exchange'], 'order_initiated_exchange')
        self.assertEqual(kwargs['routing_key'], 'order_initiated_routing_key')

        # Check message content
        message = kwargs['message']
        self.assertIn('order', message)
        order = message['order']
        self.assertEqual(order['id'], order_info['id'])
        self.assertEqual(order['status'], 'INICIADO')
        self.assertEqual(len(order['items']), 2)


if __name__ == '__main__':
    unittest.main()