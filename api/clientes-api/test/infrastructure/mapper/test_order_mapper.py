import unittest
from datetime import datetime
from unittest.mock import Mock, patch

from src.domain.entities.order_dto import OrderDTO
from src.infrastructure.mapper.order_mapper import OrderMapper
from src.infrastructure.model.order_model import OrderModel, OrderStatusEnum


class TestOrderMapper(unittest.TestCase):
    def setUp(self):
        # Create a sample OrderModel
        self.mock_order_model = Mock(spec=OrderModel)
        self.mock_order_model.id = "order123"
        self.mock_order_model.client_id = "client456"
        self.mock_order_model.quantity = 5
        self.mock_order_model.subtotal = 100.0
        self.mock_order_model.tax = 10.0
        self.mock_order_model.total = 110.0
        self.mock_order_model.currency = "USD"
        self.mock_order_model.salesman_id = "sales789"
        self.mock_order_model.status = OrderStatusEnum.PENDIENTE
        self.mock_order_model.created_at = datetime(2023, 1, 1, 12, 0, 0)
        self.mock_order_model.updated_at = datetime(2023, 1, 2, 12, 0, 0)
        self.mock_order_model.order_details = []
        self.mock_order_model.client_info = None
        self.mock_order_model.payment = None

        # Create a sample OrderDTO
        self.mock_order_dto = OrderDTO(
            id="order123",
            client_id="client456",
            quantity=5,
            subtotal=100.0,
            tax=10.0,
            total=110.0,
            currency="USD",
            salesman_id="sales789",
            status="PENDING",
            created_at="2023-01-01T12:00:00",
            updated_at="2023-01-02T12:00:00"
        )
        self.mock_order_dto.order_details = []
        self.mock_order_dto.client_info = None
        self.mock_order_dto.payment = None

    @patch('src.infrastructure.mapper.order_details_mapper.OrderDetailsMapper.to_dto_list')
    @patch('src.infrastructure.mapper.client_info_mapper.ClientInfoMapper.to_dto')
    @patch('src.infrastructure.mapper.payment_mapper.PaymentMapper.to_dto')
    def test_to_dto(self, mock_payment_mapper, mock_client_info_mapper, mock_order_details_mapper):
        # Setup
        mock_order_details_mapper.return_value = []
        mock_client_info_mapper.return_value = None
        mock_payment_mapper.return_value = None

        # Execute
        result = OrderMapper.to_dto(self.mock_order_model)

        # Verify
        self.assertEqual(result.id, self.mock_order_model.id)
        self.assertEqual(result.client_id, self.mock_order_model.client_id)
        self.assertEqual(result.quantity, self.mock_order_model.quantity)
        self.assertEqual(result.subtotal, self.mock_order_model.subtotal)
        self.assertEqual(result.tax, self.mock_order_model.tax)
        self.assertEqual(result.total, self.mock_order_model.total)
        self.assertEqual(result.currency, self.mock_order_model.currency)
        self.assertEqual(result.salesman_id, self.mock_order_model.salesman_id)
        self.assertEqual(result.status, self.mock_order_model.status.value)
        self.assertEqual(result.created_at, self.mock_order_model.created_at.isoformat())
        self.assertEqual(result.updated_at, self.mock_order_model.updated_at.isoformat())

    def test_to_dto_none(self):
        # Execute
        result = OrderMapper.to_dto(None)

        # Verify
        self.assertIsNone(result)

    def test_to_single_dto(self):
        # Execute
        result = OrderMapper.to_single_dto(self.mock_order_model)

        # Verify
        self.assertEqual(result.id, self.mock_order_model.id)
        self.assertEqual(result.client_id, self.mock_order_model.client_id)
        self.assertIsNone(result.order_details)
        self.assertIsNone(result.client_info)
        self.assertIsNone(result.payment)

    def test_to_single_dto_none(self):
        # Execute
        result = OrderMapper.to_single_dto(None)

        # Verify
        self.assertIsNone(result)

    @patch('src.infrastructure.mapper.order_details_mapper.OrderDetailsMapper.to_model_list')
    @patch('src.infrastructure.mapper.client_info_mapper.ClientInfoMapper.to_model')
    @patch('src.infrastructure.mapper.payment_mapper.PaymentMapper.to_model')
    def test_to_model(self, mock_payment_mapper, mock_client_info_mapper, mock_order_details_mapper):
        # Setup
        mock_order_details_mapper.return_value = []
        mock_client_info_mapper.return_value = None
        mock_payment_mapper.return_value = None

        # Execute
        result = OrderMapper.to_model(self.mock_order_dto)

        # Verify
        self.assertEqual(result.id, self.mock_order_dto.id)
        self.assertEqual(result.client_id, self.mock_order_dto.client_id)
        self.assertEqual(result.quantity, self.mock_order_dto.quantity)
        self.assertEqual(result.subtotal, self.mock_order_dto.subtotal)
        self.assertEqual(result.tax, self.mock_order_dto.tax)
        self.assertEqual(result.total, self.mock_order_dto.total)
        self.assertEqual(result.currency, self.mock_order_dto.currency)
        self.assertEqual(result.salesman_id, self.mock_order_dto.salesman_id)
        self.assertEqual(result.status, self.mock_order_dto.status)
        self.assertEqual(result.created_at, datetime.fromisoformat(self.mock_order_dto.created_at))
        self.assertEqual(result.updated_at, datetime.fromisoformat(self.mock_order_dto.updated_at))

    def test_to_model_none(self):
        # Execute
        result = OrderMapper.to_model(None)

        # Verify
        self.assertIsNone(result)

    def test_to_dto_list(self):
        # Setup
        models = [self.mock_order_model, self.mock_order_model]

        # Mock to_dto method
        with patch.object(OrderMapper, 'to_dto', return_value=self.mock_order_dto) as mock_to_dto:
            # Execute
            result = OrderMapper.to_dto_list(models)

            # Verify
            self.assertEqual(len(result), 2)
            self.assertEqual(mock_to_dto.call_count, 2)
            self.assertEqual(result[0], self.mock_order_dto)
            self.assertEqual(result[1], self.mock_order_dto)

    def test_to_dto_single_list(self):
        # Setup
        models = [self.mock_order_model, self.mock_order_model]

        # Mock to_single_dto method
        with patch.object(OrderMapper, 'to_single_dto', return_value=self.mock_order_dto) as mock_to_single_dto:
            # Execute
            result = OrderMapper.to_dto_single_list(models)

            # Verify
            self.assertEqual(len(result), 2)
            self.assertEqual(mock_to_single_dto.call_count, 2)
            self.assertEqual(result[0], self.mock_order_dto)
            self.assertEqual(result[1], self.mock_order_dto)


if __name__ == '__main__':
    unittest.main()