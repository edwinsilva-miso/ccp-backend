import logging

from .errors.errors import RecordNotExistsError
from ..domain.entities.client_visit_record_dto import ClientVisitRecordDTO

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)
logger = logging.getLogger(__name__)


class GetClientVisitRecord:
    """
    Use case for retrieving a client visit record.
    """

    def __init__(self, client_visit_repository):
        """
        Initialize the use case with a client visit repository.
        :param client_visit_repository: Repository for client visit operations.
        """
        self.client_visit_repository = client_visit_repository

    def execute(self, record_id: str) -> ClientVisitRecordDTO:
        """
        Retrieve a client visit record by salesman and client ID.
        :param record_id: ID of the client visit record.
        :return: Client visit record associated with the salesman and client.
        """
        logger.debug(f"Retrieving client visit record: {record_id}")

        # Retrieve the client visit record
        response = self.client_visit_repository.get_visit_record(record_id)
        if not response:
            logger.error(f"Client visit record {record_id} not found.")
            raise RecordNotExistsError

        logger.debug(f"Client visit record retrieved successfully: {response.__str__()}")
        return response
