import logging

from ...application.errors.errors import ResourceNotFoundError
from ...domain.repositories.warehouse_repository import WarehouseRepository

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class DeleteWarehouse:
    """
    Use case for deleting a warehouse by its ID.
    """

    def __init__(self, warehouse_repository: WarehouseRepository):
        """
        Initialize the use case with a warehouse repository.
        
        :param warehouse_repository: Repository for warehouse operations
        """
        self.warehouse_repository = warehouse_repository

    def execute(self, warehouse_id: str) -> bool:
        """
        Execute the use case to delete a warehouse by its ID.
        
        :param warehouse_id: ID of the warehouse to delete
        :return: True if deleted successfully
        :raises ResourceNotFoundError: If the warehouse doesn't exist
        """
        logger.debug(f"[DELETE_WAREHOUSE] Starting deletion of warehouse with ID: {warehouse_id}")
        
        # Check if the warehouse exists
        existing_warehouse = self.warehouse_repository.get_by_id(warehouse_id)
        if not existing_warehouse:
            logger.error(f"[DELETE_WAREHOUSE] Warehouse with ID {warehouse_id} not found")
            raise ResourceNotFoundError
        
        # Delete the warehouse using the repository
        result = self.warehouse_repository.delete(warehouse_id)
        
        if result:
            logger.debug(f"[DELETE_WAREHOUSE] Successfully deleted warehouse with ID: {warehouse_id}")
        else:
            logger.error(f"[DELETE_WAREHOUSE] Failed to delete warehouse with ID: {warehouse_id}")
            
        return result