from ..dao.selling_plan_dao import SellingPlanDAO
from ..mapper.selling_plan_mapper import SellingPlanMapper
from ...domain.entities.selling_plan_dto import SellingPlanDTO
from ...domain.repositories.selling_plan_repository import SellingPlanRepository


class SellingPlanAdapter(SellingPlanRepository):
    """
    Adapter for SellingPlanRepository to interact with SellingPlanDAO and SellingPlanMapper.
    """

    def get_by_id(self, plan_id: str) -> SellingPlanDTO | None:
        """
        Retrieves a selling plan by its ID.
        """
        selling_plan = SellingPlanDAO.get_by_id(plan_id)
        return SellingPlanMapper.to_dto(selling_plan) if selling_plan else None

    def get_by_user_id(self, user_id: str) -> list[SellingPlanDTO]:
        """
        Retrieves all selling plans for a given user.
        """
        selling_plan_list = SellingPlanDAO.get_by_user_id(user_id)
        return SellingPlanMapper.to_dto_list(selling_plan_list)

    def add(self, selling_plan_dto: SellingPlanDTO) -> SellingPlanDTO:
        """
        Adds a new Selling Plan.
        """
        selling_plan = SellingPlanMapper.to_model(selling_plan_dto)
        selling_plan_dao = SellingPlanDAO.save(selling_plan)
        return SellingPlanMapper.to_dto(selling_plan_dao)

    def update(self, selling_plan_dto: SellingPlanDTO) -> SellingPlanDTO:
        """
        Updates an existing Selling Plan.
        """
        selling_plan = SellingPlanMapper.to_model(selling_plan_dto)
        selling_plan_dao = SellingPlanDAO.update(selling_plan)
        return SellingPlanMapper.to_dto(selling_plan_dao)

    def delete(self, plan_id: str) -> bool:
        """
        Deletes a Selling Plan by its ID.
        """
        return SellingPlanDAO.delete(plan_id)