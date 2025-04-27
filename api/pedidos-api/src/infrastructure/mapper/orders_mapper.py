from datetime import datetime

from .order_history_mapper import OrderHistoryMapper
from .order_item_mapper import OrderItemMapper
from ..model.orders_model import OrderModel
from ...domain.entities.order_dto import OrderDTO


class OrderMapper:

    @staticmethod
    def to_dto(order_model: OrderModel) -> OrderDTO | None:
        """
        Convert OrderModel to OrderDTO.
        :param order_model: The OrderModel object to convert.
        :return: The converted OrderDTO object.
        """
        if order_model is None:
            return None

        order_date = order_model.order_date.isoformat() if order_model.order_date else None
        transaction_date = order_model.transaction_date.isoformat() if order_model.transaction_date else None
        created_at = order_model.created_at.isoformat() if order_model.created_at else None
        updated_at = order_model.updated_at.isoformat() if order_model.updated_at else None

        return OrderDTO(
            id=order_model.id,
            order_date=order_date,
            status=order_model.status,
            subtotal=order_model.subtotal,
            taxes=order_model.taxes,
            total=order_model.total,
            currency=order_model.currency,
            client_id=order_model.client_id,
            payment_id=order_model.payment_id,
            transaction_status=order_model.transaction_status,
            transaction_date=transaction_date,
            transaction_id=order_model.transaction_id,
            order_items=OrderItemMapper.to_list_dto(order_model.order_items),
            order_history=OrderHistoryMapper.to_list_dto(order_model.order_history),
            created_at=created_at,
            updated_at=updated_at
        )

    @staticmethod
    def to_single_dto(order_model: OrderModel) -> OrderDTO | None:
        """
        Convert a single OrderModel to OrderDTO.
        :param order_model: The OrderModel object to convert.
        :return: The converted OrderDTO object.
        """
        if order_model is None:
            return None

        order_date = order_model.order_date.isoformat() if order_model.order_date else None
        transaction_date = order_model.transaction_date.isoformat() if order_model.transaction_date else None
        created_at = order_model.created_at.isoformat() if order_model.created_at else None
        updated_at = order_model.updated_at.isoformat() if order_model.updated_at else None

        return OrderDTO(
            id=order_model.id,
            order_date=order_date,
            status=order_model.status,
            subtotal=order_model.subtotal,
            taxes=order_model.taxes,
            total=order_model.total,
            currency=order_model.currency,
            client_id=order_model.client_id,
            payment_id=order_model.payment_id,
            transaction_status=order_model.transaction_status,
            transaction_date=transaction_date,
            transaction_id=order_model.transaction_id,
            order_items=[],
            order_history=[],
            created_at=created_at,
            updated_at=updated_at
        )

    @staticmethod
    def to_model(order_dto: OrderDTO) -> OrderModel | None:
        """
        Convert OrderDTO to OrderModel.
        :param order_dto: The OrderDTO object to convert.
        :return: The converted OrderModel object.
        """

        if order_dto is None:
            return None

        order_date = datetime.fromisoformat(order_dto.order_date) if order_dto.order_date and isinstance(
            order_dto.order_date,
            str) else order_dto.order_date
        transaction_date = datetime.fromisoformat(
            order_dto.transaction_date) if order_dto.transaction_date and isinstance(
            order_dto.transaction_date,
            str) else order_dto.transaction_date

        created_at = datetime.fromisoformat(order_dto.created_at) if order_dto.created_at and isinstance(
            order_dto.created_at,
            str) else order_dto.created_at
        updated_at = datetime.fromisoformat(order_dto.updated_at) if order_dto.updated_at and isinstance(
            order_dto.updated_at,
            str) else order_dto.updated_at

        return OrderModel(
            id=order_dto.id,
            order_date=order_date,
            status=order_dto.status,
            subtotal=order_dto.subtotal,
            taxes=order_dto.taxes,
            total=order_dto.total,
            currency=order_dto.currency,
            client_id=order_dto.client_id,
            payment_id=order_dto.payment_id,
            transaction_status=order_dto.transaction_status,
            transaction_date=transaction_date,
            transaction_id=order_dto.transaction_id,
            order_items=OrderItemMapper.to_list_model(order_dto.order_items),
            order_history=OrderHistoryMapper.to_list_model(order_dto.order_history),
            created_at=created_at,
            updated_at=updated_at
        )

    @staticmethod
    def to_model_list(order_dtos: list[OrderDTO]) -> list[OrderModel]:
        """
        Convert a list of OrderDTO to a list of OrderModel.
        :param order_dtos: The list of OrderDTO objects to convert.
        :return: The converted list of OrderModel objects.
        """
        return [OrderMapper.to_model(order_dto) for order_dto in order_dtos]

    @staticmethod
    def to_dto_list(order_models: list[OrderModel]) -> list[OrderDTO]:
        """
        Convert a list of OrderModel to a list of OrderDTO.
        :param order_models: The list of OrderModel objects to convert.
        :return: The converted list of OrderDTO objects.
        """
        return [OrderMapper.to_single_dto(order_model) for order_model in order_models]
