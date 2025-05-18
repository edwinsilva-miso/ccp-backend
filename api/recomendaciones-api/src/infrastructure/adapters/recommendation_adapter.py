from ..dao.recommendation_result_dao import RecommendationResultDAO
from ..mapper.recommendation_result_mapper import RecommendationResultMapper
from ...domain.entities.recommentation_result_dto import RecommendationResultDTO
from ...domain.repositories.recommendation_repository import RecommendationRepository


class RecommendationAdapter(RecommendationRepository):
    """
    Adapter class to handle the interaction with the recommendation results in the database.
    """

    def __init__(self):
        self.dao = RecommendationResultDAO()
        self.mapper = RecommendationResultMapper()

    def add(self, recommendation_result_dto: RecommendationResultDTO) -> RecommendationResultDTO:
        """
        Add a new recommendation result after the optimization algorithm finalizes the calculation
        :param recommendation_result_dto: The recommendation result to be saved on database
        :return The recommendation saved
        """
        model = self.mapper.to_model(recommendation_result_dto)
        created_model = self.dao.create(model)
        return self.mapper.to_dto(created_model)

    def get_all(self) -> list[RecommendationResultDTO]:
        """
        Retrieves all recommendations made for every product at the CCP system
        :return the list of saved recommendations
        """
        models = self.dao.find_all()
        return self.mapper.to_dto_list(models)
