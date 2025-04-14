import logging

from ..domain.entities.provider_dto import ProviderDTO

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)
logger = logging.getLogger(__name__)


class GetProviderByNit:
    """
    Use case for retrieving a provider by its NIT.
    """

    def __init__(self, provider_repository):
        """
        Initializes the GetProviderById use case with a provider repository.
        :param provider_repository: An instance of ProviderDTORepository.
        """
        self.provider_repository = provider_repository

    def execute(self, nit: str) -> ProviderDTO:
        """
        Retrieves a provider by its NIT from the repository.
        :param nit: The NIT of the provider to retrieve.
        :return: A ProviderDTO object representing the provider.
        """
        logging.debug(f"Retrieving provider with NIT {nit}...")
        return self.provider_repository.get_by_nit(nit)
