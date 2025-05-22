import logging

from ...application.errors.errors import ResourceNotFoundError
from ...domain.repositories.warehouse_stock_item_repository import WarehouseStockItemRepository

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class DeleteWarehouseStockItem:
    """
    Use case for deleting a warehouse stock item by its ID.
    """

    def __init__(self, warehouse_stock_item_repository: WarehouseStockItemRepository):
        """
        Initialize the use case with a warehouse stock item repository.
        
        :param warehouse_stock_item_repository: Repository for warehouse stock item operations
        """
        self.warehouse_stock_item_repository = warehouse_stock_item_repository

    def execute(self, item_id: str) -> bool:
        """
        Execute the use case to delete a warehouse stock item by its ID.
        
        :param item_id: ID of the warehouse stock item to delete
        :return: True if deleted successfully
        :raises ResourceNotFoundError: If the warehouse stock item doesn't exist
        """
        logger.debug(f"[DELETE_WAREHOUSE_STOCK_ITEM] Starting deletion of warehouse stock item with ID: {item_id}")
        
        # Check if the warehouse stock item exists
        existing_warehouse_stock_item = self.warehouse_stock_item_repository.get_by_id(item_id)
        if not existing_warehouse_stock_item:
            logger.error(f"[DELETE_WAREHOUSE_STOCK_ITEM] Warehouse stock item with ID {item_id} not found")
            raise ResourceNotFoundError
        
        # Delete the warehouse stock item using the repository
        result = self.warehouse_stock_item_repository.delete(item_id)
        
        if result:
            logger.debug(f"[DELETE_WAREHOUSE_STOCK_ITEM] Successfully deleted warehouse stock item with ID: {item_id}")
        else:
            logger.error(f"[DELETE_WAREHOUSE_STOCK_ITEM] Failed to delete warehouse stock item with ID: {item_id}")
            
        return result