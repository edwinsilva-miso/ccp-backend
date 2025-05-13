import logging

from ..domain.entities.warehouse_dto import WarehouseDTO
from ..domain.repositories.warehouse_repository import WarehouseRepository

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class GetAllWarehouses:
    """
    Use case for retrieving all warehouses.
    """

    def __init__(self, warehouse_repository: WarehouseRepository):
        """
        Initialize the use case with a warehouse repository.
        
        :param warehouse_repository: Repository for warehouse operations
        """
        self.warehouse_repository = warehouse_repository

    def execute(self) -> list[WarehouseDTO]:
        """
        Execute the use case to retrieve all warehouses.
        
        :return: List of warehouse DTOs
        """
        logger.debug("[GET_ALL_WAREHOUSES] Starting retrieval of all warehouses")
        
        # Get all warehouses using the repository
        warehouses = self.warehouse_repository.get_all()
        
        logger.debug(f"[GET_ALL_WAREHOUSES] Successfully retrieved {len(warehouses)} warehouses")
        return warehouses