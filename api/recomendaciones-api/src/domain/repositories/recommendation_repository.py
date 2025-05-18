from abc import ABC, abstractmethod
from ..entities.recommentation_result_dto import RecommendationResultDTO

class RecommendationRepository(ABC):

    @abstractmethod
    def add(self, recommendation_result_dto: RecommendationResultDTO) -> RecommendationResultDTO:
        """
        Add a new recommendation result after the optimization algorithm finalizes the calculation
        :param recommendation_result_dto: The recommendation result to be saved on database
        :return The recommendation saved
        """
        pass

    @abstractmethod
    def get_all(self) -> list[RecommendationResultDTO]:
        """
        Retrieves all recommendations made for every product at the CCP system
        :return the list of saved recommendations
        """
        pass
