from ..model.client_salesman_model import ClientSalesmanModel
from ...domain.entities.client_salesman_dto import ClientSalesmanDTO


class ClientSalesmanMapper:
    """
    Mapper class to convert between ClientSalesmanDTO and ClientSalesmanModel.
    """

    @staticmethod
    def to_dto(model: ClientSalesmanModel) -> ClientSalesmanDTO:
        """
        Convert a ClientSalesmanModel to a ClientSalesmanDTO.
        :param model: ClientSalesmanModel to convert.
        :return: Converted ClientSalesmanDTO.
        """
        return ClientSalesmanDTO(
            id=str(model.id),
            salesman_id=str(model.salesman_id),
            client_id=str(model.client_id),
            client_name=model.client_name,
            client_phone=model.client_phone,
            client_email=model.client_email,
            address=model.address,
            city=model.city,
            country=model.country,
            store_name=model.store_name
        )

    @staticmethod
    def to_model(dto: ClientSalesmanDTO) -> ClientSalesmanModel:
        """
        Convert a ClientSalesmanDTO to a ClientSalesmanModel.
        :param dto: ClientSalesmanDTO to convert.
        :return: Converted ClientSalesmanModel.
        """
        return ClientSalesmanModel(
            id=dto.id,
            salesman_id=dto.salesman_id,
            client_id=dto.client_id,
            client_name=dto.client_name,
            client_phone=dto.client_phone,
            client_email=dto.client_email,
            address=dto.address,
            city=dto.city,
            country=dto.country,
            store_name=dto.store_name
        )

    @staticmethod
    def to_dto_list(models: list[ClientSalesmanModel]) -> list[ClientSalesmanDTO]:
        """
        Convert a list of ClientSalesmanModel to a list of ClientSalesmanDTO.
        :param models: List of ClientSalesmanModel to convert.
        :return: List of converted ClientSalesmanDTO.
        """
        return [ClientSalesmanMapper.to_dto(model) for model in models]

    @staticmethod
    def to_model_list(dtos: list[ClientSalesmanDTO]) -> list[ClientSalesmanModel]:
        """
        Convert a list of ClientSalesmanDTO to a list of ClientSalesmanModel.
        :param dtos: List of ClientSalesmanDTO to convert.
        :return: List of converted ClientSalesmanModel.
        """
        return [ClientSalesmanMapper.to_model(dto) for dto in dtos]
