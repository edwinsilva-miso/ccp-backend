import logging

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)
logger = logging.getLogger(__name__)


class GetClientsBySalesman:
    """
    Use case for retrieving all clients associated with a specific salesman.
    """

    def __init__(self, client_repository):
        """
        Initialize the use case with a client repository.
        :param client_repository: Repository for client operations.
        """
        self.client_repository = client_repository

    def execute(self, salesman_id: str):
        """
        Get all clients by salesman ID.
        :param salesman_id: ID of the salesman to retrieve
        :return: List of clients associated with the salesman.
        """
        logger.debug(f"Getting clients for salesman ID: {salesman_id}")
        clients = self.client_repository.get_clients_salesman(salesman_id)
        logger.debug(f"Clients retrieved: {clients}")
        return clients
