import logging

from ..domain.entities.provider_dto import ProviderDTO

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)
logger = logging.getLogger(__name__)


class GetAllProviders:
    """
    Use case for retrieving all providers.
    """

    def __init__(self, provider_repository):
        """
        Initializes the GetProviderById use case with a provider repository.
        :param provider_repository: An instance of ProviderDTORepository.
        """
        self.provider_repository = provider_repository

    def execute(self) -> list[ProviderDTO]:
        """
        Retrieves all providers from the repository.
        :return: A list of ProviderDTO objects.
        """
        logging.debug("Retrieving all providers...")
        return self.provider_repository.get_all()
