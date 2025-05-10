from datetime import datetime

from .client_info_mapper import ClientInfoMapper
from .order_details_mapper import OrderDetailsMapper
from .payment_mapper import PaymentMapper
from ...domain.entities.order_dto import OrderDTO
from ...infrastructure.model.order_model import OrderModel


class OrderMapper:
    """
    Mapper class to convert between OrderDTO and OrderModel.
    """

    @staticmethod
    def to_dto(model: OrderModel) -> OrderDTO | None:
        """
        Convert OrderModel to OrderDTO.
        :param model: The OrderModel instance to convert.
        :return: An OrderDTO instance.
        """
        if model is None:
            return None

        created_at = model.created_at.isoformat() if model.created_at else None
        updated_at = model.updated_at.isoformat() if model.updated_at else None

        dto = OrderDTO(
            id=model.id,
            client_id=model.client_id,
            quantity=model.quantity,
            subtotal=model.subtotal,
            tax=model.tax,
            total=model.total,
            currency=model.currency,
            status=model.status.value,
            created_at=created_at,
            updated_at=updated_at,
        )
        dto.order_details = OrderDetailsMapper.to_dto_list(model.order_details)
        dto.client_info = ClientInfoMapper.to_dto(model.client_info)
        dto.payment = PaymentMapper.to_dto(model.payment)

        return dto

    @staticmethod
    def to_single_dto(model: OrderModel) -> OrderDTO | None:
        """
        Convert OrderModel to single OrderDTO.
        :param model: The OrderModel instance to convert.
        :return: An OrderDTO instance.
        """
        if model is None:
            return None

        created_at = model.created_at.isoformat() if model.created_at else None
        updated_at = model.updated_at.isoformat() if model.updated_at else None

        dto = OrderDTO(
            id=model.id,
            client_id=model.client_id,
            quantity=model.quantity,
            subtotal=model.subtotal,
            tax=model.tax,
            total=model.total,
            currency=model.currency,
            status=model.status.value,
            created_at=created_at,
            updated_at=updated_at,
        )
        dto.order_details = None
        dto.client_info = None
        dto.payment = None

        return dto

    @staticmethod
    def to_model(dto: OrderDTO) -> OrderModel | None:
        """
        Convert OrderDTO to OrderModel.
        :param dto: The OrderDTO instance to convert.
        :return: An OrderModel instance.
        """
        if dto is None:
            return None

        created_at = datetime.fromisoformat(dto.created_at) if dto.created_at and isinstance(dto.created_at,
                                                                                             str) else dto.created_at
        updated_at = datetime.fromisoformat(dto.updated_at) if dto.updated_at and isinstance(dto.updated_at,
                                                                                             str) else dto.updated_at

        return OrderModel(
            id=dto.id,
            client_id=dto.client_id,
            quantity=dto.quantity,
            subtotal=dto.subtotal,
            tax=dto.tax,
            total=dto.total,
            currency=dto.currency,
            status=dto.status,
            created_at=created_at,
            updated_at=updated_at,
            order_details=OrderDetailsMapper.to_model_list(dto.order_details),
            client_info=ClientInfoMapper.to_model(dto.client_info),
            payment=PaymentMapper.to_model(dto.payment),
        )

    @staticmethod
    def to_dto_list(models: list[OrderModel]) -> list[OrderDTO]:
        """
        Convert a list of OrderModel to a list of OrderDTO.
        :param models: The list of OrderModel instances to convert.
        :return: A list of OrderDTO instances.
        """
        return [OrderMapper.to_dto(model) for model in models]

    @staticmethod
    def to_dto_single_list(models: list[OrderModel]) -> list[OrderDTO]:
        """
        Convert a list of OrderModel to a list of OrderDTO.
        :param models: The list of OrderModel instances to convert.
        :return: A list of OrderDTO instances.
        """
        return [OrderMapper.to_single_dto(model) for model in models]
