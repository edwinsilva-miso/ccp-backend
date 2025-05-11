from ..database.declarative_base import Session
from ..model.selling_plan_model import SellingPlanModel


class SellingPlanDAO:
    """
    Data Access Object (DAO) for SellingPlanModel.
    Provides an interface to interact with the database.
    """

    @classmethod
    def save(cls, selling_plan: SellingPlanModel) -> SellingPlanModel:
        """
        Create a new selling plan record in the database.
        :param selling_plan: SellingPlanModel to save.
        :return: The saved SellingPlanModel with its ID.
        """
        session = Session()
        session.add(selling_plan)
        session.commit()
        session.refresh(selling_plan)
        session.close()
        return selling_plan

    @classmethod
    def update(cls, selling_plan: SellingPlanModel) -> SellingPlanModel:
        """
        Update an existing selling plan record in the database.
        :param selling_plan: SellingPlanModel to update.
        :return: The updated SellingPlanModel.
        """
        session = Session()
        merged_plan = session.merge(selling_plan)
        session.commit()
        session.refresh(merged_plan)
        session.close()
        return merged_plan

    @classmethod
    def delete(cls, plan_id: str) -> bool:
        """
        Delete a selling plan record from the database.
        :param plan_id: ID of the selling plan to delete.
        :return: True if deleted successfully, False otherwise.
        """
        session = Session()
        selling_plan = session.query(SellingPlanModel).filter(SellingPlanModel.id == plan_id).first()
        if selling_plan:
            session.delete(selling_plan)
            session.commit()
            session.close()
            return True
        session.close()
        return False

    @classmethod
    def get_by_id(cls, plan_id: str) -> SellingPlanModel | None:
        """
        Get a selling plan record by ID.
        :param plan_id: ID of the selling plan to retrieve.
        :return: SellingPlanModel if found, None otherwise.
        """
        session = Session()
        selling_plan = session.query(SellingPlanModel).filter(SellingPlanModel.id == plan_id).first()
        session.close()
        return selling_plan

    @classmethod
    def get_by_user_id(cls, user_id: str) -> list[SellingPlanModel]:
        """
        Get all selling plan records by user ID.
        :param user_id: ID of the user to retrieve selling plans for.
        :return: List of SellingPlanModel with the specified user ID.
        """
        session = Session()
        selling_plans = session.query(SellingPlanModel).filter(SellingPlanModel.user_id == user_id).all()
        session.close()
        return selling_plans