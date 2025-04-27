from ...domain.entities.order_details_dto import OrderDetailsDTO
from ...infrastructure.model.order_details_model import OrderDetailsModel


class OrderDetailsMapper:
    """
    Mapper class to convert between OrderDetailsDTO and OrderDetailsModel.
    """

    @staticmethod
    def to_dto(model: OrderDetailsModel) -> OrderDetailsDTO:
        """
        Convert OrderDetailsModel to OrderDetailsDTO.
        :param model: The OrderDetailsModel instance to convert.
        :return: An OrderDetailsDTO instance.
        """
        return OrderDetailsDTO(
            id=str(model.id),
            order_id=model.order_id,
            product_id=model.product_id,
            quantity=model.quantity,
            unit_price=model.unit_price,
            total_price=model.total_price,
            currency=model.currency
        )

    @staticmethod
    def to_model(dto: OrderDetailsDTO) -> OrderDetailsModel:
        """
        Convert OrderDetailsDTO to OrderDetailsModel.
        :param dto: The OrderDetailsDTO instance to convert.
        :return: An OrderDetailsModel instance.
        """
        return OrderDetailsModel(
            id=dto.id,
            order_id=dto.order_id,
            product_id=dto.product_id,
            quantity=dto.quantity,
            unit_price=dto.unit_price,
            total_price=dto.total_price,
            currency=dto.currency
        )

    @staticmethod
    def to_dto_list(models: list[OrderDetailsModel]) -> list[OrderDetailsDTO]:
        """
        Convert a list of OrderDetailsModel to a list of OrderDetailsDTO.
        :param models: The list of OrderDetailsModel instances to convert.
        :return: A list of OrderDetailsDTO instances.
        """
        return [OrderDetailsMapper.to_dto(model) for model in models]

    @staticmethod
    def to_model_list(dtos: list[OrderDetailsDTO]) -> list[OrderDetailsModel]:
        """
        Convert a list of OrderDetailsDTO to a list of OrderDetailsModel.
        :param dtos: The list of OrderDetailsDTO instances to convert.
        :return: A list of OrderDetailsModel instances.
        """
        return [OrderDetailsMapper.to_model(dto) for dto in dtos]
