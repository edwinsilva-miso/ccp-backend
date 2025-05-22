import logging

from ..domain.entities.recommentation_result_dto import RecommendationResultDTO

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)
logger = logging.getLogger(__name__)


class GetAllRecommendations:
    """
    Class to handle the retrieval of all recommendations
    """

    def __init__(self, recommendation_repository):
        """
        Initialize the GetAllRecommendations class
        :param recommendation_repository: The repository to handle recommendations
        """
        self.recommendation_repository = recommendation_repository

    def execute(self) -> list[RecommendationResultDTO]:
        """
        Execute the retrieval of all recommendations
        :return: The list of saved recommendations
        """
        logger.debug("Starting the retrieval of all recommendations")

        # Retrieve all recommendations from the repository
        recommendations = self.recommendation_repository.get_all()
        logger.info("Retrieval of all recommendations completed successfully")
        return recommendations
