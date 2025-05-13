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


class UpdateWarehouseStockItem:
    """
    Use case for updating an existing warehouse stock item.
    """

    def __init__(self, warehouse_stock_item_repository: WarehouseStockItemRepository):
        """
        Initialize the use case with a warehouse stock item repository.
        
        :param warehouse_stock_item_repository: Repository for warehouse stock item operations
        """
        self.warehouse_stock_item_repository = warehouse_stock_item_repository

    def execute(self, warehouse_stock_item_dto: WarehouseStockItemDTO) -> WarehouseStockItemDTO:
        """
        Execute the use case to update an existing warehouse stock item.
        
        :param warehouse_stock_item_dto: DTO containing updated warehouse stock item data
        :return: Updated warehouse stock item DTO
        :raises ResourceNotFoundError: If the warehouse stock item doesn't exist
        """
        logger.debug(f"[UPDATE_WAREHOUSE_STOCK_ITEM] Starting update of warehouse stock item with ID: {warehouse_stock_item_dto.id}")
        
        # Check if the warehouse stock item exists
        existing_warehouse_stock_item = self.warehouse_stock_item_repository.get_by_id(warehouse_stock_item_dto.id)
        if not existing_warehouse_stock_item:
            logger.error(f"[UPDATE_WAREHOUSE_STOCK_ITEM] Warehouse stock item with ID {warehouse_stock_item_dto.id} not found")
            raise ResourceNotFoundError
        
        # Update the warehouse stock item using the repository
        updated_warehouse_stock_item = self.warehouse_stock_item_repository.update(warehouse_stock_item_dto)
        
        logger.debug(f"[UPDATE_WAREHOUSE_STOCK_ITEM] Successfully updated warehouse stock item with ID: {updated_warehouse_stock_item.id}")
        return updated_warehouse_stock_item