from datetime import datetime
from ...domain.entities.reports.order_reports_dto import OrderReportsDTO
from ...infrastructure.model.order_reports_model import OrderReportsModel

class OrderReportsMapper:
    """
    Mapper class to convert between OrderReportsModel and ReportResponseDTO.
    """

    @staticmethod
    def to_dto(model: OrderReportsModel) -> OrderReportsDTO | None:
        """
        Convert OrderReportsModel to ReportResponseDTO.
        :param model: The OrderReportsModel instance to convert.
        :return: A ReportResponseDTO instance.
        """
        if model is None:
            return None

        dto = OrderReportsDTO(
            report_id=model.id,
            user_id=model.user_id,
            report_name=model.name,
            report_date=model.date.isoformat() if model.date else None,
            url=model.url
        )

        return dto

    @staticmethod
    def to_model(dto: OrderReportsDTO) -> OrderReportsModel | None:
        """
        Convert ReportResponseDTO to OrderReportsModel.
        :param dto: The ReportResponseDTO instance to convert.
        :return: An OrderReportsModel instance.
        """
        if dto is None:
            return None

        date = datetime.fromisoformat(dto.report_date) if dto.report_date and isinstance(dto.report_date, str) else dto.report_date

        model = OrderReportsModel(
            id=dto.report_id,
            user_id=dto.user_id,
            name=dto.report_name,
            date=date,
            url=dto.url
        )

        return model

    @staticmethod
    def to_dto_list(models: list[OrderReportsModel]) -> list[OrderReportsDTO]:
        """
        Convert a list of OrderReportsModel to a list of ReportResponseDTO.
        :param models: The list of OrderReportsModel instances to convert.
        :return: A list of ReportResponseDTO instances.
        """
        return [OrderReportsMapper.to_dto(model) for model in models]

    @staticmethod
    def to_model_list(dtos: list[OrderReportsDTO]) -> list[OrderReportsModel]:
        """
        Convert a list of ReportResponseDTO to a list of OrderReportsModel.
        :param dtos: The list of ReportResponseDTO instances to convert.
        :return: A list of OrderReportsModel instances.
        """
        return [OrderReportsMapper.to_model(dto) for dto in dtos]