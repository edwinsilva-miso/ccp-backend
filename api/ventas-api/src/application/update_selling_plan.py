import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

from ..domain.entities.selling_plan_dto import SellingPlanDTO
from .errors.errors import ResourceNotFoundError


class UpdateSellingPlan:
    """
    Use case for updating an existing selling plan.
    """

    def __init__(self, selling_plan_repository):
        """
        Initialize the use case with a selling plan repository.
        :param selling_plan_repository: Repository for selling plan operations.
        """
        self.selling_plan_repository = selling_plan_repository

    def execute(self, data: SellingPlanDTO) -> SellingPlanDTO:
        """
        Update an existing selling plan.
        :param data: Instance of SellingPlanDTO containing updated selling plan information.
        :return: Updated SellingPlanDTO.
        :raises: ResourceNotFoundError if the selling plan does not exist.
        """
        logger.debug(f"Updating selling plan: {data.__repr__()}")

        # Check if the selling plan exists
        existing_plan = self.selling_plan_repository.get_by_id(data.id)
        if not existing_plan:
            logger.error(f"Selling plan with ID {data.id} not found.")
            raise ResourceNotFoundError

        # Update the selling plan
        response = self.selling_plan_repository.update(data)
        logger.debug(f"Selling plan updated successfully: {response.__repr__()}")
        return response