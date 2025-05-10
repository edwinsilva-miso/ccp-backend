from ..model.order_history_model import OrderHistoryModel
from ...domain.entities.order_history_dto import OrderHistoryDTO


class OrderHistoryMapper:
    """
    Mapper class for converting between OrderHistoryModel and OrderHistoryDTO.
    """

    @staticmethod
    def to_dto(order_history_model: OrderHistoryModel) -> OrderHistoryDTO:
        """
        Convert OrderHistoryModel to OrderHistoryDTO.
        :param order_history_model: The OrderHistoryModel object to convert.
        :return: The converted OrderHistoryDTO object.
        """
        return OrderHistoryDTO(
            id=order_history_model.id,
            order_id=order_history_model.order_id,
            status=order_history_model.status,
            description=order_history_model.description,
            date=order_history_model.date.isoformat() if order_history_model.date else None
        )

    @staticmethod
    def to_model(order_history_dto: OrderHistoryDTO) -> OrderHistoryModel:
        """
        Convert OrderHistoryDTO to OrderHistoryModel.
        :param order_history_dto: The OrderHistoryDTO object to convert.
        :return: The converted OrderHistoryModel object.
        """
        return OrderHistoryModel(
            id=order_history_dto.id,
            order_id=order_history_dto.order_id,
            status=order_history_dto.status,
            description=order_history_dto.description,
            date=order_history_dto.date
        )

    @staticmethod
    def to_list_dto(order_history_models: list[OrderHistoryModel]) -> list[OrderHistoryDTO]:
        """
        Convert a list of OrderHistoryModel to a list of OrderHistoryDTO.
        :param order_history_models: The list of OrderHistoryModel objects to convert.
        :return: The converted list of OrderHistoryDTO objects.
        """
        return [OrderHistoryMapper.to_dto(order_history_model) for order_history_model in order_history_models]

    @staticmethod
    def to_list_model(order_history_dtos: list[OrderHistoryDTO]) -> list[OrderHistoryModel]:
        """
        Convert a list of OrderHistoryDTO to a list of OrderHistoryModel.
        :param order_history_dtos: The list of OrderHistoryDTO objects to convert.
        :return: The converted list of OrderHistoryModel objects.
        """
        return [OrderHistoryMapper.to_model(order_history_dto) for order_history_dto in order_history_dtos]
