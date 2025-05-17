import logging
from ..domain.entities.reports.order_reports_dto import OrderReportsDTO

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)
logger = logging.getLogger(__name__)

class GetReportsByUser:
    """
    Use case for retrieving reports by user ID.
    """

    def __init__(self, order_reports_repository):
        self.order_reports_repository = order_reports_repository

    def execute(self, user_id: str) -> list[OrderReportsDTO]:
        """
        Retrieve reports associated with the given user ID.
        :param user_id: The unique identifier of the user.
        :return: List of OrderReportsDTO objects associated with the user.
        """
        logger.debug("Retrieving reports for user ID: %s", user_id)
        reports = self.order_reports_repository.get_by_user_id(user_id)
        return reports