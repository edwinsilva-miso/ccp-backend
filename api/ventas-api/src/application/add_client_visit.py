import logging

from ..domain.entities.client_visit_record_dto import ClientVisitRecordDTO

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)
logger = logging.getLogger(__name__)


class AddClientVisit:
    """
    Use case for adding a client visit record.
    """

    def __init__(self, client_visit_repository):
        """
        Initialize the use case with a client visit repository.
        :param client_visit_repository: Repository for client visit operations.
        """
        self.client_visit_repository = client_visit_repository

    def execute(self, data: ClientVisitRecordDTO) -> str:
        """
        Add a new client visit record.
        :param data: Instance of ClientVisitRecordDTO containing visit information.
        :return: ID of the added client visit record.
        """
        logger.debug(f"Adding client visit record: {data.__str__()}")

        # Add the new client visit record
        response = self.client_visit_repository.add_visit_record(data)
        logger.debug(f"Client visit record added successfully: {response.__str__()}")
        return response
