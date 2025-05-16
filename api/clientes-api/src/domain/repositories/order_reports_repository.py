from abc import ABC, abstractmethod
from ..entities.reports.order_reports_dto import OrderReportsDTO
class OrderReportsRepository(ABC):

    @abstractmethod
    def add(self, dto: OrderReportsDTO) -> OrderReportsDTO:
        """
        Add a new order report to the repository.
        :param dto: The ReportResponseDTO instance to add.
        :return: The added ReportResponseDTO instance.
        """
        pass

    @abstractmethod
    def get_by_user_id(self, user_id: str) -> list[OrderReportsDTO]:
        """
        Get all order reports by user ID.
        :param user_id: The ID of the user to find order reports for.
        :return: A list of ReportResponseDTO instances if found.
        """
        pass