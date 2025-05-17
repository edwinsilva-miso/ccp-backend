from datetime import datetime

from ..model.client_visit_record_model import ClientVisitRecordModel
from ...domain.entities.client_visit_record_dto import ClientVisitRecordDTO

class ClientVisitRecordMapper:
    """
    Mapper class for converting between ClientVisitRecordModel and ClientVisitRecordDTO.
    This class provides methods to convert the database model to a DTO and vice versa.
    """

    @staticmethod
    def to_dto(model: ClientVisitRecordModel) -> ClientVisitRecordDTO:
        """
        Convert a ClientVisitRecordModel instance to a ClientVisitRecordDTO instance.
        :param model: The ClientVisitRecordModel instance to convert.
        :return: A ClientVisitRecordDTO instance.
        """
        return ClientVisitRecordDTO(
            record_id=str(model.id),
            client_id=str(model.client_id),
            salesman_id=str(model.salesman_id),
            visit_date=model.visit_date.isoformat() if model.visit_date else None,
            notes=model.notes
        )

    @staticmethod
    def to_model(dto: ClientVisitRecordDTO) -> ClientVisitRecordModel:
        """
        Convert a ClientVisitRecordDTO instance to a ClientVisitRecordModel instance.
        :param dto: The ClientVisitRecordDTO instance to convert.
        :return: A ClientVisitRecordModel instance.
        """
        visit_date = datetime.fromisoformat(dto.visit_date) if dto.visit_date else None

        return ClientVisitRecordModel(
            id=dto.record_id,
            client_id=dto.client_id,
            salesman_id=dto.salesman_id,
            visit_date=visit_date,
            notes=dto.notes
        )

    @staticmethod
    def to_dto_list(models: list[ClientVisitRecordModel]) -> list[ClientVisitRecordDTO]:
        """
        Convert a list of ClientVisitRecordModel instances to a list of ClientVisitRecordDTO instances.
        :param models: The list of ClientVisitRecordModel instances to convert.
        :return: A list of ClientVisitRecordDTO instances.
        """
        return [ClientVisitRecordMapper.to_dto(model) for model in models]

    @staticmethod
    def to_model_list(dtos: list[ClientVisitRecordDTO]) -> list[ClientVisitRecordModel]:
        """
        Convert a list of ClientVisitRecordDTO instances to a list of ClientVisitRecordModel instances.
        :param dtos: The list of ClientVisitRecordDTO instances to convert.
        :return: A list of ClientVisitRecordModel instances.
        """
        return [ClientVisitRecordMapper.to_model(dto) for dto in dtos]