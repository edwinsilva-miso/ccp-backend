import logging
import re

from .errors.errors import InvalidFormatError, ProviderAlreadyExistsError
from .utils import constants
from ..domain.entities.provider_dto import ProviderDTO

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)
logger = logging.getLogger(__name__)


class CreateProvider:
    """
    Use case for creating a new provider.
    """

    def __init__(self, provider_repository):
        """
        Initializes the CreateProvider use case with a provider repository.
        :param provider_repository: An instance of ProviderDTORepository.
        """
        self.provider_repository = provider_repository

    def execute(self, provider: ProviderDTO) -> str:
        """
        Creates a new provider in the repository.
        :param provider: A ProviderDTO object representing the provider to create.
        :return: The ID of the created provider.
        """
        logging.debug(f"Creating provider: {provider.__str__()}")

        logging.debug("Validating provider information...")
        nit_pattern = constants.NIT_PATTERN
        email_pattern = constants.EMAIL_PATTERN

        if not re.match(nit_pattern, provider.nit) or not re.match(email_pattern, provider.email):
            logging.error("Invalid NIT or email format.")
            raise InvalidFormatError

        logging.debug(f"Checking if provider {provider.nit} already exists...")
        existing_provider = self.provider_repository.get_by_nit(provider.nit)
        if existing_provider:
            logging.error(f"Provider {provider.nit} already exists.")
            raise ProviderAlreadyExistsError

        logging.debug(f"Creating provider {provider.nit}...")
        return self.provider_repository.add(provider)
