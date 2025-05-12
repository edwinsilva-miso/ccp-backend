import logging
from ..model.selling_plan_model import SellingPlanModel
from ...domain.entities.selling_plan_dto import SellingPlanDTO

logger = logging.getLogger(__name__)


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
        logger.debug(f"converting selling plan model to dto: {model.__dict__}")
        dto = SellingPlanDTO(
            id=str(model.id),
            user_id=str(model.user_id),
            title=model.title,
            description=model.description,
            target_amount=model.target_amount,
            target_date=model.target_date,
            status=model.status,
            created_at=model.created_at.isoformat() if model.created_at else None
        )
        logger.debug(f"successfully converted to dto: {dto.__dict__}")
        return dto

    @staticmethod
    def to_model(dto: SellingPlanDTO) -> SellingPlanModel:
        """
        Convert a SellingPlanDTO to a SellingPlanModel.
        :param dto: SellingPlanDTO to convert.
        :return: Converted SellingPlanModel.
        """
        logger.debug(f"converting selling plan dto to model: {dto.__dict__}")
        model = SellingPlanModel(
            id=dto.id,
            user_id=dto.user_id,
            title=dto.title,
            description=dto.description,
            target_amount=dto.target_amount,
            target_date=dto.target_date,
            status=dto.status
        )
        logger.debug(f"successfully converted to model: {model.__dict__}")
        return model

    @staticmethod
    def to_dto_list(models: list[SellingPlanModel]) -> list[SellingPlanDTO]:
        """
        Convert a list of SellingPlanModel to a list of SellingPlanDTO.
        :param models: List of SellingPlanModel to convert.
        :return: List of converted SellingPlanDTO.
        """
        logger.debug(f"converting list of {len(models)} selling plan models to dtos")
        dtos = [SellingPlanMapper.to_dto(model) for model in models]
        logger.debug(f"successfully converted {len(dtos)} models to dtos")
        return dtos

    @staticmethod
    def to_model_list(dtos: list[SellingPlanDTO]) -> list[SellingPlanModel]:
        """
        Convert a list of SellingPlanDTO to a list of SellingPlanModel.
        :param dtos: List of SellingPlanDTO to convert.
        :return: List of converted SellingPlanModel.
        """
        logger.debug(f"converting list of {len(dtos)} selling plan dtos to models")
        models = [SellingPlanMapper.to_model(dto) for dto in dtos]
        logger.debug(f"successfully converted {len(models)} dtos to models")
        return models
