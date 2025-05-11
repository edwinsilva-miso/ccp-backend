from ..model.selling_plan_model import SellingPlanModel
from ...domain.entities.selling_plan_dto import SellingPlanDTO


class SellingPlanMapper:
    """
    Mapper class to convert between SellingPlanDTO and SellingPlanModel.
    """

    @staticmethod
    def to_dto(model: SellingPlanModel) -> SellingPlanDTO:
        """
        Convert a SellingPlanModel to a SellingPlanDTO.
        :param model: SellingPlanModel to convert.
        :return: Converted SellingPlanDTO.
        """
        return SellingPlanDTO(
            id=str(model.id),
            user_id=str(model.user_id),
            title=model.title,
            description=model.description,
            target_amount=model.target_amount,
            target_date=model.target_date,
            status=model.status,
            created_at=model.created_at.isoformat() if model.created_at else None
        )

    @staticmethod
    def to_model(dto: SellingPlanDTO) -> SellingPlanModel:
        """
        Convert a SellingPlanDTO to a SellingPlanModel.
        :param dto: SellingPlanDTO to convert.
        :return: Converted SellingPlanModel.
        """
        return SellingPlanModel(
            id=dto.id,
            user_id=dto.user_id,
            title=dto.title,
            description=dto.description,
            target_amount=dto.target_amount,
            target_date=dto.target_date,
            status=dto.status
        )

    @staticmethod
    def to_dto_list(models: list[SellingPlanModel]) -> list[SellingPlanDTO]:
        """
        Convert a list of SellingPlanModel to a list of SellingPlanDTO.
        :param models: List of SellingPlanModel to convert.
        :return: List of converted SellingPlanDTO.
        """
        return [SellingPlanMapper.to_dto(model) for model in models]

    @staticmethod
    def to_model_list(dtos: list[SellingPlanDTO]) -> list[SellingPlanModel]:
        """
        Convert a list of SellingPlanDTO to a list of SellingPlanModel.
        :param dtos: List of SellingPlanDTO to convert.
        :return: List of converted SellingPlanModel.
        """
        return [SellingPlanMapper.to_model(dto) for dto in dtos]