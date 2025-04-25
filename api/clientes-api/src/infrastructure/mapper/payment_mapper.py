from datetime import datetime

from ..model.payment_model import PaymentModel
from ...domain.entities.payment_dto import PaymentDTO


class PaymentMapper:

    @staticmethod
    def to_dto(payment_model: PaymentModel) -> PaymentDTO | None:
        """Convert a PaymentModel to a PaymentDTO"""
        if not payment_model:
            return None

        transaction_date = payment_model.transaction_date.isoformat() if payment_model.transaction_date else None

        dto = PaymentDTO(
            id=payment_model.id,
            order_id=payment_model.order_id,
            amount=payment_model.amount,
            card_number=payment_model.card_number,
            cvv="***",
            expiry_date="*****",
            currency=payment_model.currency
        )
        dto.payment_method = payment_model.payment_method if isinstance(payment_model.payment_method,
                                                                        str) else payment_model.payment_method.value,
        dto.transaction_id = payment_model.transaction_id,
        dto.status = payment_model.status if isinstance(payment_model.status, str) else payment_model.status.value,
        dto.transaction_date = transaction_date

        return dto

    @staticmethod
    def to_model(payment_dto: PaymentDTO) -> PaymentModel | None:
        """Convert a PaymentDTO to a PaymentModel"""
        if not payment_dto:
            return None

        transaction_date = datetime.fromisoformat(payment_dto.transaction_date) if isinstance(
            payment_dto.transaction_date,
            str) else payment_dto.transaction_date

        return PaymentModel(
            id=payment_dto.id,
            order_id=payment_dto.order_id,
            amount=payment_dto.amount,
            card_number=payment_dto.card_number,
            currency=payment_dto.currency,
            payment_method=payment_dto.payment_method,
            transaction_id=payment_dto.transaction_id,
            status=payment_dto.status,
            transaction_date=transaction_date
        )
