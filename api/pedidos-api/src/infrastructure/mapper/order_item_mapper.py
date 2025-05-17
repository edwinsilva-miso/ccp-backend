from ..model.order_item_model import OrderItemsModel
from ...domain.entities.order_item_dto import OrderItemDTO


class OrderItemMapper:
    """
    Mapper class for converting between OrderItemModel and OrderItemDTO.
    """

    @staticmethod
    def to_dto(order_item_model: OrderItemsModel) -> OrderItemDTO:
        """
        Convert OrderItemModel to OrderItemDTO.
        :param order_item_model: The OrderItemModel object to convert.
        :return: The converted OrderItemDTO object.
        """
        return OrderItemDTO(
            id=order_item_model.id,
            order_id=order_item_model.order_id,
            product_id=order_item_model.product_id,
            quantity=order_item_model.quantity,
            unit_price=order_item_model.unit_price,
            total_price=order_item_model.total_price,
            currency=order_item_model.currency
        )

    @staticmethod
    def to_model(order_item_dto: OrderItemDTO) -> OrderItemsModel:
        """
        Convert OrderItemDTO to OrderItemModel.
        :param order_item_dto: The OrderItemDTO object to convert.
        :return: The converted OrderItemModel object.
        """
        return OrderItemsModel(
            id=order_item_dto.id,
            order_id=order_item_dto.order_id,
            product_id=order_item_dto.product_id,
            quantity=order_item_dto.quantity,
            unit_price=order_item_dto.unit_price,
            total_price=order_item_dto.total_price,
            currency=order_item_dto.currency
        )

    @staticmethod
    def to_list_dto(order_item_models: list[OrderItemsModel]) -> list[OrderItemDTO]:
        """
        Convert a list of OrderItemModel to a list of OrderItemDTO.
        :param order_item_models: The list of OrderItemModel objects to convert.
        :return: The converted list of OrderItemDTO objects.
        """
        return [OrderItemMapper.to_dto(order_item_model) for order_item_model in order_item_models]

    @staticmethod
    def to_list_model(order_item_dtos: list[OrderItemDTO]) -> list[OrderItemsModel]:
        """
        Convert a list of OrderItemDTO to a list of OrderItemModel.
        :param order_item_dtos: The list of OrderItemDTO objects to convert.
        :return: The converted list of OrderItemModel objects.
        """
        return [OrderItemMapper.to_model(order_item_dto) for order_item_dto in order_item_dtos]
