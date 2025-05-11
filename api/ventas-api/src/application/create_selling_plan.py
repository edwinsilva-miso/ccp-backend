import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

from ..domain.entities.selling_plan_dto import SellingPlanDTO


class CreateSellingPlan:
    """
    Use case for creating a new selling plan.
    """

    def __init__(self, selling_plan_repository):
        """
        Initialize the use case with a selling plan repository.
        :param selling_plan_repository: Repository for selling plan operations.
        """
        self.selling_plan_repository = selling_plan_repository

    def execute(self, data: SellingPlanDTO) -> SellingPlanDTO:
        """
        Create a new selling plan.
        :param data: Instance of SellingPlanDTO containing selling plan information.
        :return: Created SellingPlanDTO.
        """
        logger.debug(f"Creating selling plan: {data.__repr__()}")

        # Add the new selling plan
        response = self.selling_plan_repository.add(data)
        logger.debug(f"Selling plan created successfully: {response.__repr__()}")
        return response