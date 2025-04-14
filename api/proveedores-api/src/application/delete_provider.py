import logging

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)
logger = logging.getLogger(__name__)

class DeleteProvider:
    """
    Use case for deleting a provider by its ID.
    """

    def __init__(self, provider_repository):
        """
        Initializes the DeleteProvider use case with a provider repository.
        :param provider_repository: An instance of ProviderRepository.
        """
        self.provider_repository = provider_repository

    def execute(self, id: str) -> None:
        """
        Deletes a provider by its ID from the repository.
        :param id: The ID of the provider to delete.
        """
        logging.debug(f"Deleting provider with ID {id}...")
        self.provider_repository.delete(id)
