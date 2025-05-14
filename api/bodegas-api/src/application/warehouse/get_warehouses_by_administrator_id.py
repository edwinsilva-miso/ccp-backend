import logging

from ...domain.entities.warehouse_dto import WarehouseDTO
from ...domain.repositories.warehouse_repository import WarehouseRepository

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class GetWarehousesByAdministratorId:
    """
    Use case for retrieving all warehouses for a specific administrator.
    """

    def __init__(self, warehouse_repository: WarehouseRepository):
        """
        Initialize the use case with a warehouse repository.
        
        :param warehouse_repository: Repository for warehouse operations
        """
        self.warehouse_repository = warehouse_repository

    def execute(self, administrator_id: str) -> list[WarehouseDTO]:
        """
        Execute the use case to retrieve all warehouses for a specific administrator.
        
        :param administrator_id: ID of the administrator
        :return: List of warehouse DTOs
        """
        logger.debug(f"[GET_WAREHOUSES_BY_ADMINISTRATOR_ID] Starting retrieval of warehouses for administrator ID: {administrator_id}")
        
        # Get warehouses by administrator ID using the repository
        warehouses = self.warehouse_repository.get_by_administrator_id(administrator_id)
        
        logger.debug(f"[GET_WAREHOUSES_BY_ADMINISTRATOR_ID] Successfully retrieved {len(warehouses)} warehouses for administrator ID: {administrator_id}")
        return warehouses