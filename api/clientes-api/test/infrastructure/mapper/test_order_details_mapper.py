import unittest
from unittest.mock import Mock
import uuid

from src.domain.entities.order_details_dto import OrderDetailsDTO
from src.infrastructure.mapper.order_details_mapper import OrderDetailsMapper
from src.infrastructure.model.order_details_model import OrderDetailsModel


class TestOrderDetailsMapper(unittest.TestCase):
    def setUp(self):
        # Create sample UUID for testing
        self.test_id = uuid.uuid4()

        # Create sample model
        self.mock_order_details_model = Mock(spec=OrderDetailsModel)
        self.mock_order_details_model.id = self.test_id
        self.mock_order_details_model.order_id = "order123"
        self.mock_order_details_model.product_id = "product456"
        self.mock_order_details_model.quantity = 3.0
        self.mock_order_details_model.unit_price = 10.5
        self.mock_order_details_model.total_price = 31.5
        self.mock_order_details_model.currency = "USD"

        # Create sample DTO
        self.mock_order_details_dto = OrderDetailsDTO(
            id=str(self.test_id),
            order_id="order123",
            product_id="product456",
            quantity=3.0,
            unit_price=10.5,
            total_price=31.5,
            currency="USD"
        )

    def test_to_dto(self):
        # Execute
        result = OrderDetailsMapper.to_dto(self.mock_order_details_model)

        # Verify
        self.assertEqual(result.id, str(self.mock_order_details_model.id))
        self.assertEqual(result.order_id, self.mock_order_details_model.order_id)
        self.assertEqual(result.product_id, self.mock_order_details_model.product_id)
        self.assertEqual(result.quantity, self.mock_order_details_model.quantity)
        self.assertEqual(result.unit_price, self.mock_order_details_model.unit_price)
        self.assertEqual(result.total_price, self.mock_order_details_model.total_price)
        self.assertEqual(result.currency, self.mock_order_details_model.currency)

    def test_to_model(self):
        # Execute
        result = OrderDetailsMapper.to_model(self.mock_order_details_dto)

        # Verify
        self.assertEqual(result.id, self.mock_order_details_dto.id)
        self.assertEqual(result.order_id, self.mock_order_details_dto.order_id)
        self.assertEqual(result.product_id, self.mock_order_details_dto.product_id)
        self.assertEqual(result.quantity, self.mock_order_details_dto.quantity)
        self.assertEqual(result.unit_price, self.mock_order_details_dto.unit_price)
        self.assertEqual(result.total_price, self.mock_order_details_dto.total_price)
        self.assertEqual(result.currency, self.mock_order_details_dto.currency)

    def test_to_dto_list(self):
        # Setup
        models = [self.mock_order_details_model, self.mock_order_details_model]

        # Execute
        result = OrderDetailsMapper.to_dto_list(models)

        # Verify
        self.assertEqual(len(result), 2)
        for dto in result:
            self.assertEqual(dto.id, str(self.mock_order_details_model.id))
            self.assertEqual(dto.order_id, self.mock_order_details_model.order_id)
            self.assertEqual(dto.product_id, self.mock_order_details_model.product_id)
            self.assertEqual(dto.quantity, self.mock_order_details_model.quantity)
            self.assertEqual(dto.unit_price, self.mock_order_details_model.unit_price)
            self.assertEqual(dto.total_price, self.mock_order_details_model.total_price)
            self.assertEqual(dto.currency, self.mock_order_details_model.currency)

    def test_to_model_list(self):
        # Setup
        dtos = [self.mock_order_details_dto, self.mock_order_details_dto]

        # Execute
        result = OrderDetailsMapper.to_model_list(dtos)

        # Verify
        self.assertEqual(len(result), 2)
        for model in result:
            self.assertEqual(model.id, self.mock_order_details_dto.id)
            self.assertEqual(model.order_id, self.mock_order_details_dto.order_id)
            self.assertEqual(model.product_id, self.mock_order_details_dto.product_id)
            self.assertEqual(model.quantity, self.mock_order_details_dto.quantity)
            self.assertEqual(model.unit_price, self.mock_order_details_dto.unit_price)
            self.assertEqual(model.total_price, self.mock_order_details_dto.total_price)
            self.assertEqual(model.currency, self.mock_order_details_dto.currency)

    def test_to_dto_none(self):
        # Unlike ClientInfoMapper, the OrderDetailsMapper doesn't handle None values
        # This test is to ensure the code raises an appropriate error
        with self.assertRaises(AttributeError):
            OrderDetailsMapper.to_dto(None)

    def test_to_model_none(self):
        # This test is to ensure the code raises an appropriate error
        with self.assertRaises(AttributeError):
            OrderDetailsMapper.to_model(None)


if __name__ == '__main__':
    unittest.main()