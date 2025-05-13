import logging

from ...application.errors.errors import ResourceNotFoundError
from ...domain.entities.warehouse_stock_item_dto import WarehouseStockItemDTO
from ...domain.repositories.warehouse_stock_item_repository import WarehouseStockItemRepository

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class GetWarehouseStockItemById:
    """
    Use case for retrieving a warehouse stock item by its ID.
    """

    def __init__(self, warehouse_stock_item_repository: WarehouseStockItemRepository):
        """
        Initialize the use case with a warehouse stock item repository.
        
        :param warehouse_stock_item_repository: Repository for warehouse stock item operations
        """
        self.warehouse_stock_item_repository = warehouse_stock_item_repository

    def execute(self, item_id: str) -> WarehouseStockItemDTO:
        """
        Execute the use case to retrieve a warehouse stock item by its ID.
        
        :param item_id: ID of the warehouse stock item to retrieve
        :return: Retrieved warehouse stock item DTO
        :raises ResourceNotFoundError: If the warehouse stock item doesn't exist
        """
        logger.debug(f"[GET_WAREHOUSE_STOCK_ITEM_BY_ID] Starting retrieval of warehouse stock item with ID: {item_id}")
        
        # Get the warehouse stock item using the repository
        warehouse_stock_item = self.warehouse_stock_item_repository.get_by_id(item_id)
        
        # Check if the warehouse stock item exists
        if not warehouse_stock_item:
            logger.error(f"[GET_WAREHOUSE_STOCK_ITEM_BY_ID] Warehouse stock item with ID {item_id} not found")
            raise ResourceNotFoundError
        
        logger.debug(f"[GET_WAREHOUSE_STOCK_ITEM_BY_ID] Successfully retrieved warehouse stock item with ID: {warehouse_stock_item.id}")
        return warehouse_stock_item