import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

from .errors.errors import ResourceNotFoundError


class DeleteSellingPlan:
    """
    Use case for deleting a selling plan.
    """

    def __init__(self, selling_plan_repository):
        """
        Initialize the use case with a selling plan repository.
        :param selling_plan_repository: Repository for selling plan operations.
        """
        self.selling_plan_repository = selling_plan_repository

    def execute(self, plan_id: str) -> bool:
        """
        Delete a selling plan by its ID.
        :param plan_id: ID of the selling plan to delete.
        :return: True if deleted successfully.
        :raises: ResourceNotFoundError if the selling plan does not exist.
        """
        logger.debug(f"Deleting selling plan with ID: {plan_id}")

        # Check if the selling plan exists
        existing_plan = self.selling_plan_repository.get_by_id(plan_id)
        if not existing_plan:
            logger.error(f"Selling plan with ID {plan_id} not found.")
            raise ResourceNotFoundError

        # Delete the selling plan
        result = self.selling_plan_repository.delete(plan_id)
        if result:
            logger.debug(f"Selling plan with ID {plan_id} deleted successfully.")
        else:
            logger.error(f"Failed to delete selling plan with ID {plan_id}.")
            
        return result