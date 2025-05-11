import logging

from ..dao.selling_plan_dao import SellingPlanDAO
from ..mapper.selling_plan_mapper import SellingPlanMapper
from ...domain.entities.selling_plan_dto import SellingPlanDTO
from ...domain.repositories.selling_plan_repository import SellingPlanRepository

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class SellingPlanAdapter(SellingPlanRepository):
    """
    Adapter for SellingPlanRepository to interact with SellingPlanDAO and SellingPlanMapper.
    """

    def get_by_id(self, plan_id: str) -> SellingPlanDTO | None:
        """
        Retrieves a selling plan by its ID.
        """
        logger.debug(f"[GET_BY_ID] Starting retrieval operation for selling plan ID: {plan_id}")
        selling_plan = SellingPlanDAO.get_by_id(plan_id)
        if selling_plan:
            logger.debug(
                f"[GET_BY_ID] Successfully retrieved plan - Title: {selling_plan.title} | Status: {selling_plan.status} | User: {selling_plan.user_id}")
            return SellingPlanMapper.to_dto(selling_plan)
        logger.debug(f"[GET_BY_ID] No selling plan found in database with ID: {plan_id}")
        return None

    def get_by_user_id(self, user_id: str) -> list[SellingPlanDTO]:
        """
        Retrieves all selling plans for a given user.
        """
        logger.debug(f"[GET_BY_USER] Beginning retrieval of all selling plans for User ID: {user_id}")
        selling_plan_list = SellingPlanDAO.get_by_user_id(user_id)
        logger.debug(
            f"[GET_BY_USER] Retrieved {len(selling_plan_list)} selling plans | Active Plans: {sum(1 for plan in selling_plan_list if plan.status == 'active')}")
        return SellingPlanMapper.to_dto_list(selling_plan_list)

    def add(self, selling_plan_dto: SellingPlanDTO) -> SellingPlanDTO:
        """
        Adds a new Selling Plan.
        """
        logger.debug(
            f"[ADD_PLAN] Initiating creation of new selling plan - Title: {selling_plan_dto.title} | User: {selling_plan_dto.user_id}")
        selling_plan = SellingPlanMapper.to_model(selling_plan_dto)
        logger.debug(
            f"[ADD_PLAN] Successfully mapped DTO to model - Target Amount: {selling_plan_dto.target_amount} | Target Date: {selling_plan_dto.target_date}")
        selling_plan_dao = SellingPlanDAO.save(selling_plan)
        logger.debug(
            f"[ADD_PLAN] Plan successfully persisted in database with ID: {selling_plan_dao.id} | Status: {selling_plan_dao.status}")
        return SellingPlanMapper.to_dto(selling_plan_dao)

    def update(self, selling_plan_dto: SellingPlanDTO) -> SellingPlanDTO:
        """
        Updates an existing Selling Plan.
        """
        logger.debug(
            f"[UPDATE_SELLING_PLAN] Starting update process for plan ID: {selling_plan_dto.id} | User ID: {selling_plan_dto.user_id} | Title: {selling_plan_dto.title}")
        selling_plan = SellingPlanMapper.to_model(selling_plan_dto)
        logger.debug(
            f"[UPDATE_SELLING_PLAN] Successfully mapped DTO to model - Status: {selling_plan_dto.status} | Target Amount: {selling_plan_dto.target_amount} | Target Date: {selling_plan_dto.target_date}")
        selling_plan_dao = SellingPlanDAO.update(selling_plan)
        logger.debug(
            f"[UPDATE_SELLING_PLAN] Database update completed successfully for plan ID: {selling_plan_dto.id} | New Status: {selling_plan_dao.status}")
        return SellingPlanMapper.to_dto(selling_plan_dao)

    def delete(self, plan_id: str) -> bool:
        """
        Deletes a Selling Plan by its ID.
        """
        logger.debug(f"[DELETE_PLAN] Starting deletion process for selling plan ID: {plan_id}")
        result = SellingPlanDAO.delete(plan_id)
        logger.debug(f"[DELETE_PLAN] Deletion operation completed - Success: {result} | Plan ID: {plan_id}")
        return result
