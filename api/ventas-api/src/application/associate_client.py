import logging

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)
logger = logging.getLogger(__name__)

from ..domain.entities.client_salesman_dto import ClientSalesmanDTO
from .errors.errors import ClientAlreadyAssociatedError


class AssociateClient:
    """
    Use case for associating a client with a salesman.
    """

    def __init__(self, client_repository):
        """
        Initialize the use case with a client repository.
        :param client_repository: Repository for client operations.
        """
        self.client_repository = client_repository

    def execute(self, data: ClientSalesmanDTO) -> ClientSalesmanDTO:
        """
        Associate a client with a salesman.
        :param data: Instance of ClientSalesmanDTO containing client information.
        :return: ID of the associated client.
        """
        logger.debug(f"Associating client: {data.__str__()}")

        # Check if the client already exists
        existing_client = self.client_repository.get_client_by_id(data.client_id)
        if existing_client:
            logger.error(f"Client {data.client_id} already associated.")
            raise ClientAlreadyAssociatedError

        # Add the new client
        response = self.client_repository.add(data)
        logger.debug(f"Client associated successfully: {response.__str__()}")
        return response
