import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

from ..domain.entities.selling_plan_dto import SellingPlanDTO
from .errors.errors import ResourceNotFoundError


class GetSellingPlanById:
    """
    Use case for retrieving a selling plan by its ID.
    """

    def __init__(self, selling_plan_repository):
        """
        Initialize the use case with a selling plan repository.
        :param selling_plan_repository: Repository for selling plan operations.
        """
        logger.debug("initializing get selling plan by id use case")
        self.selling_plan_repository = selling_plan_repository
        logger.debug(f"selling plan repository instance set: {selling_plan_repository.__class__.__name__}")

    def execute(self, plan_id: str) -> SellingPlanDTO:
        """
        Retrieve a selling plan by its ID.
        :param plan_id: ID of the selling plan to retrieve.
        :return: SellingPlanDTO if found.
        :raises: ResourceNotFoundError if the selling plan does not exist.
        """
        logger.debug(f"attempting to retrieve selling plan with id: {plan_id}")

        # Get the selling plan
        logger.debug(f"calling repository method get_by_id for plan id: {plan_id}")
        selling_plan = self.selling_plan_repository.get_by_id(plan_id)
        if not selling_plan:
            logger.error(f"selling plan with id {plan_id} not found in repository")
            raise ResourceNotFoundError

        logger.debug(f"successfully retrieved selling plan from repository: {selling_plan.__repr__()}")
        return selling_plan