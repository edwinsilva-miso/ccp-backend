from ..model.client_info_model import ClientInfoModel
from ...domain.entities.client_info_dto import ClientInfoDTO

class ClientInfoMapper:
    """
    Mapper class to convert between ClientInfoDTO and ClientInfoModel.
    """

    @staticmethod
    def to_dto(model: ClientInfoModel) -> ClientInfoDTO | None:
        """
        Convert ClientInfoModel to ClientInfoDTO.
        :param model: The ClientInfoModel instance to convert.
        :return: A ClientInfoDTO instance.
        """
        if model is None:
            return None

        return ClientInfoDTO(
            name=model.name,
            address=model.address,
            phone=model.phone,
            email=model.email,
            order_id=model.order_id
        )

    @staticmethod
    def to_model(dto: ClientInfoDTO) -> ClientInfoModel | None:
        """
        Convert ClientInfoDTO to ClientInfoModel.
        :param dto: The ClientInfoDTO instance to convert.
        :return: A ClientInfoModel instance.
        """
        if dto is None:
            return None

        return ClientInfoModel(
            name=dto.name,
            address=dto.address,
            phone=dto.phone,
            email=dto.email,
            order_id=dto.order_id
        )