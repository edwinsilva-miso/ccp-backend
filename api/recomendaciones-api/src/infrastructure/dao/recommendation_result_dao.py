from ..database.declarative_base import Session
from ..model.recommendation_result_model import RecommendationResultModel


class RecommendationResultDAO:
    """
    Data Access Object (DAO) for RecommendationResultModel.
    This class provides methods to interact with the recommendation_results table in the database.
    """

    @classmethod
    def create(cls, recommendation_result: RecommendationResultModel) -> RecommendationResultModel:
        """
        Create a new recommendation result in the database.
        :param recommendation_result: The recommendation result to create.
        :return: The created recommendation result.
        """
        session = Session()
        session.add(recommendation_result)
        session.commit()
        session.refresh(recommendation_result)
        session.close()
        return recommendation_result

    @classmethod
    def find_all(cls) -> list[RecommendationResultModel]:
        """
        Retrieve all recommendation results from the database.
        :return: A list of recommendation results.
        """
        session = Session()
        recommendation_results = session.query(RecommendationResultModel).all()
        session.close()
        return recommendation_results
