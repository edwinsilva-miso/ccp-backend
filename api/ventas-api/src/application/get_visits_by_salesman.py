import logging

from ..domain.entities.client_visit_record_dto import ClientVisitRecordDTO

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)
logger = logging.getLogger(__name__)


class GetVisitsBySalesman:
    """
    Use case for retrieving visits by a salesman.
    """

    def __init__(self, client_visit_repository):
        """
        Initialize the use case with a client visit repository.
        :param client_visit_repository: Repository for client visit operations.
        """
        self.client_visit_repository = client_visit_repository

    def execute(self, salesman_id: str) -> list[ClientVisitRecordDTO]:
        """
        Retrieve visits by a salesman.
        :param salesman_id: ID of the salesman.
        :return: List of client visit records associated with the salesman.
        """
        logger.debug(f"Retrieving visits for salesman: {salesman_id}")

        # Retrieve visits by salesman
        response = self.client_visit_repository.get_visit_records_by_salesman(salesman_id)
        logger.debug(f"Visits retrieved successfully: {response}")
        return response
