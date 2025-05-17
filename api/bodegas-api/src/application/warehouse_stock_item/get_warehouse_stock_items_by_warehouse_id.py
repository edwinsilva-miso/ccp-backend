import logging

from ...domain.entities.warehouse_stock_item_dto import WarehouseStockItemDTO
from ...domain.repositories.warehouse_stock_item_repository import WarehouseStockItemRepository

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class GetWarehouseStockItemsByWarehouseId:
    """
    Use case for retrieving all warehouse stock items for a given warehouse.
    """

    def __init__(self, warehouse_stock_item_repository: WarehouseStockItemRepository):
        """
        Initialize the use case with a warehouse stock item repository.
        
        :param warehouse_stock_item_repository: Repository for warehouse stock item operations
        """
        self.warehouse_stock_item_repository = warehouse_stock_item_repository

    def execute(self, warehouse_id: str) -> list[WarehouseStockItemDTO]:
        """
        Execute the use case to retrieve all warehouse stock items for a given warehouse.
        
        :param warehouse_id: ID of the warehouse
        :return: List of warehouse stock item DTOs
        """
        logger.debug(f"[GET_WAREHOUSE_STOCK_ITEMS_BY_WAREHOUSE_ID] Starting retrieval of warehouse stock items for warehouse ID: {warehouse_id}")
        
        # Get all warehouse stock items for the given warehouse using the repository
        warehouse_stock_items = self.warehouse_stock_item_repository.get_by_warehouse_id(warehouse_id)
        
        logger.debug(f"[GET_WAREHOUSE_STOCK_ITEMS_BY_WAREHOUSE_ID] Successfully retrieved {len(warehouse_stock_items)} warehouse stock items for warehouse ID: {warehouse_id}")
        return warehouse_stock_items