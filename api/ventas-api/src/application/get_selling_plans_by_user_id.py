import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

from ..domain.entities.selling_plan_dto import SellingPlanDTO


class GetSellingPlansByUserId:
    """
    Use case for retrieving all selling plans for a given user.
    """

    def __init__(self, selling_plan_repository):
        """
        Initialize the use case with a selling plan repository.
        :param selling_plan_repository: Repository for selling plan operations.
        """
        self.selling_plan_repository = selling_plan_repository

    def execute(self, user_id: str) -> list[SellingPlanDTO]:
        """
        Retrieve all selling plans for a given user.
        :param user_id: ID of the user to retrieve selling plans for.
        :return: List of SellingPlanDTO objects.
        """
        logger.debug(f"Retrieving selling plans for user with ID: {user_id}")

        # Get the selling plans
        selling_plans = self.selling_plan_repository.get_by_user_id(user_id)
        
        logger.debug(f"Retrieved {len(selling_plans)} selling plans for user with ID: {user_id}")
        return selling_plans