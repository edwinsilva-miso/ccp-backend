import logging

from ...domain.entities.warehouse_stock_item_dto import WarehouseStockItemDTO
from ...domain.repositories.warehouse_stock_item_repository import WarehouseStockItemRepository

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class CreateWarehouseStockItem:
    """
    Use case for creating a new warehouse stock item.
    """

    def __init__(self, warehouse_stock_item_repository: WarehouseStockItemRepository):
        """
        Initialize the use case with a warehouse stock item repository.
        
        :param warehouse_stock_item_repository: Repository for warehouse stock item operations
        """
        self.warehouse_stock_item_repository = warehouse_stock_item_repository

    def execute(self, warehouse_stock_item_dto: WarehouseStockItemDTO) -> WarehouseStockItemDTO:
        """
        Execute the use case to create a new warehouse stock item.
        
        :param warehouse_stock_item_dto: DTO containing warehouse stock item data
        :return: Created warehouse stock item DTO
        """
        logger.debug(f"[CREATE_WAREHOUSE_STOCK_ITEM] Starting creation of warehouse stock item for item ID: {warehouse_stock_item_dto.item_id} in warehouse: {warehouse_stock_item_dto.warehouse_id}")
        
        # Add the warehouse stock item using the repository
        created_warehouse_stock_item = self.warehouse_stock_item_repository.add(warehouse_stock_item_dto)
        
        logger.debug(f"[CREATE_WAREHOUSE_STOCK_ITEM] Successfully created warehouse stock item with ID: {created_warehouse_stock_item.warehouse_stock_item_id}")
        return created_warehouse_stock_item