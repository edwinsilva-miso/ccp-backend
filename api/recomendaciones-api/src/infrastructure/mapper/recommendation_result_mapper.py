from ..model.recommendation_result_model import RecommendationResultModel
from ...domain.entities.recommentation_result_dto import RecommendationResultDTO

class RecommendationResultMapper:
    """
    Mapper class to convert between RecommendationResultModel and RecommendationResultDTO.
    """

    @staticmethod
    def to_dto(model: RecommendationResultModel) -> RecommendationResultDTO:
        """
        Convert a RecommendationResultModel to a RecommendationResultDTO.
        :param model: The RecommendationResultModel to convert.
        :return: The converted RecommendationResultDTO.
        """
        return RecommendationResultDTO(
            id=str(model.id),
            product_id=model.product_id,
            events=model.events,
            target_sales_amount=model.target_sales_amount,
            currency=model.currency,
            recommendation=model.recommendation,
            created_at=model.created_at.isoformat() if model.created_at else None
        )

    @staticmethod
    def to_model(dto: RecommendationResultDTO) -> RecommendationResultModel:
        """
        Convert a RecommendationResultDTO to a RecommendationResultModel.
        :param dto: The RecommendationResultDTO to convert.
        :return: The converted RecommendationResultModel.
        """
        return RecommendationResultModel(
            id=dto.id,
            product_id=dto.product_id,
            events=dto.events,
            target_sales_amount=dto.target_sales_amount,
            currency=dto.currency,
            recommendation=dto.recommendation,
            created_at=dto.created_at
        )

    @staticmethod
    def to_dto_list(models: list[RecommendationResultModel]) -> list[RecommendationResultDTO]:
        """
        Convert a list of RecommendationResultModel to a list of RecommendationResultDTO.
        :param models: The list of RecommendationResultModel to convert.
        :return: The converted list of RecommendationResultDTO.
        """
        return [RecommendationResultMapper.to_dto(model) for model in models]