import logging
import re

from .errors.errors import InvalidFormatError, ProviderNotExistsError
from .utils import constants
from ..domain.entities.provider_dto import ProviderDTO

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)
logger = logging.getLogger(__name__)


class UpdateProvider:
    """
    Use case for updating an existing provider.
    """

    def __init__(self, provider_repository):
        """
        Initializes the UpdateProvider use case with a provider repository.
        :param provider_repository: An instance of ProviderDTORepository.
        """
        self.provider_repository = provider_repository

    def execute(self, id: str, provider: ProviderDTO) -> str:
        """
        Updates an existing provider in the repository.
        :param id: The ID of the provider to update.
        :param provider: A ProviderDTO object representing the updated provider data.
        :return: The ID of the updated provider.
        """
        logging.debug(f"Updating provider with ID {id}: {provider.__str__()}")
        logging.debug("Validating provider information...")
        email_pattern = constants.EMAIL_PATTERN
        if not re.match(email_pattern, provider.email):
            logging.error("Invalid email format.")
            raise InvalidFormatError

        logging.debug(f"Checking if provider with ID {id} exists...")
        existing_provider = self.provider_repository.get_by_id(id)
        if not existing_provider:
            logging.error(f"Provider with ID {id} does not exist.")
            raise ProviderNotExistsError

        logging.debug(f"Updating provider {id}...")
        return self.provider_repository.update(provider)
