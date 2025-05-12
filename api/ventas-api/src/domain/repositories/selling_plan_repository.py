from abc import ABC, abstractmethod

from ..entities.selling_plan_dto import SellingPlanDTO


class SellingPlanRepository(ABC):
    """
    Port defining the interface for Selling Plan repository.
    """

    @abstractmethod
    def get_by_id(self, plan_id: str) -> SellingPlanDTO:
        """
        Retrieves a selling plan by its ID.
        :param plan_id: ID of the selling plan
        :return: SellingPlanDTO object
        """
        pass

    @abstractmethod
    def get_by_user_id(self, user_id: str) -> list[SellingPlanDTO]:
        """
        Retrieves all selling plans for a given user.
        :param user_id: ID of the user
        :return: List of SellingPlanDTO objects
        """
        pass

    @abstractmethod
    def add(self, selling_plan_dto: SellingPlanDTO) -> SellingPlanDTO:
        """
        Adds a new Selling Plan.
        :param selling_plan_dto: SellingPlanDTO object to add
        :return: SellingPlanDTO object
        """
        pass

    @abstractmethod
    def update(self, selling_plan_dto: SellingPlanDTO) -> SellingPlanDTO:
        """
        Updates an existing Selling Plan.
        :param selling_plan_dto: SellingPlanDTO object to update
        :return: SellingPlanDTO object
        """
        pass

    @abstractmethod
    def delete(self, plan_id: str) -> bool:
        """
        Deletes a Selling Plan by its ID.
        :param plan_id: ID of the selling plan to delete
        :return: True if deleted successfully, False otherwise
        """
        pass