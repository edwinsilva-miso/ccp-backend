import unittest
from unittest.mock import Mock
from datetime import datetime
import uuid

from src.domain.entities.payment_dto import PaymentDTO
from src.infrastructure.mapper.payment_mapper import PaymentMapper
from src.infrastructure.model.payment_model import PaymentModel, PaymentStatusEnum, PaymentMethodEnum


class TestPaymentMapper(unittest.TestCase):
    def setUp(self):
        self.test_id = str(uuid.uuid4())
        self.test_date = datetime(2023, 10, 15, 12, 30, 45)
        self.test_date_iso = self.test_date.isoformat()

        # Create sample model
        self.mock_payment_model = Mock(spec=PaymentModel)
        self.mock_payment_model.id = self.test_id
        self.mock_payment_model.order_id = "order123"
        self.mock_payment_model.amount = 150.50
        self.mock_payment_model.card_number = "1234567890123456"
        self.mock_payment_model.currency = "USD"
        self.mock_payment_model.payment_method = PaymentMethodEnum.TARJETA_CREDITO
        self.mock_payment_model.transaction_id = "tr789"
        self.mock_payment_model.status = PaymentStatusEnum.APPROVED
        self.mock_payment_model.transaction_date = self.test_date

        # Create sample DTO
        self.mock_payment_dto = PaymentDTO(
            id=self.test_id,
            order_id="order123",
            amount=150.50,
            card_number="1234567890123456",
            cvv="***",
            expiry_date="*****",
            currency="USD"
        )
        self.mock_payment_dto.payment_method = PaymentMethodEnum.TARJETA_CREDITO.value
        self.mock_payment_dto.transaction_id = "tr789"
        self.mock_payment_dto.status = PaymentStatusEnum.APPROVED.value
        self.mock_payment_dto.transaction_date = self.test_date_iso

    def test_to_dto(self):
        # Execute
        result = PaymentMapper.to_dto(self.mock_payment_model)

        # Verify
        self.assertEqual(result.id, self.mock_payment_model.id)
        self.assertEqual(result.order_id, self.mock_payment_model.order_id)
        self.assertEqual(result.amount, self.mock_payment_model.amount)
        self.assertEqual(result.card_number, self.mock_payment_model.card_number)
        self.assertEqual(result.cvv, "***")
        self.assertEqual(result.expiry_date, "*****")
        self.assertEqual(result.currency, self.mock_payment_model.currency)
        self.assertEqual(result.payment_method, self.mock_payment_model.payment_method.value)
        self.assertEqual(result.transaction_id, self.mock_payment_model.transaction_id)
        self.assertEqual(result.status, self.mock_payment_model.status.value)
        self.assertEqual(result.transaction_date, self.test_date_iso)

    def test_to_dto_none(self):
        # Execute
        result = PaymentMapper.to_dto(None)

        # Verify
        self.assertIsNone(result)

    def test_to_dto_with_none_date(self):
        # Setup
        self.mock_payment_model.transaction_date = None

        # Execute
        result = PaymentMapper.to_dto(self.mock_payment_model)

        # Verify
        self.assertIsNone(result.transaction_date)
        self.assertEqual(result.id, self.mock_payment_model.id)

    def test_to_model(self):
        # Execute
        result = PaymentMapper.to_model(self.mock_payment_dto)

        # Verify
        self.assertEqual(result.id, self.mock_payment_dto.id)
        self.assertEqual(result.order_id, self.mock_payment_dto.order_id)
        self.assertEqual(result.amount, self.mock_payment_dto.amount)
        self.assertEqual(result.card_number, self.mock_payment_dto.card_number)
        self.assertEqual(result.currency, self.mock_payment_dto.currency)
        self.assertEqual(result.payment_method, self.mock_payment_dto.payment_method)
        self.assertEqual(result.transaction_id, self.mock_payment_dto.transaction_id)
        self.assertEqual(result.status, self.mock_payment_dto.status)
        self.assertEqual(result.transaction_date, self.test_date)

    def test_to_model_none(self):
        # Execute
        result = PaymentMapper.to_model(None)

        # Verify
        self.assertIsNone(result)

    def test_to_model_with_non_string_date(self):
        # Setup
        self.mock_payment_dto.transaction_date = self.test_date

        # Execute
        result = PaymentMapper.to_model(self.mock_payment_dto)

        # Verify
        self.assertEqual(result.transaction_date, self.test_date)
        self.assertEqual(result.id, self.mock_payment_dto.id)


if __name__ == '__main__':
    unittest.main()