import logging

from ..dao.warehouse_stock_item_dao import WarehouseStockItemDAO
from ..mapper.warehouse_stock_item_mapper import WarehouseStockItemMapper
from ...domain.entities.warehouse_stock_item_dto import WarehouseStockItemDTO
from ...domain.repositories.warehouse_stock_item_repository import WarehouseStockItemRepository

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class WarehouseStockItemAdapter(WarehouseStockItemRepository):
    """
    Adapter for WarehouseStockItemRepository to interact with WarehouseStockItemDAO and WarehouseStockItemMapper.
    """

    def get_by_id(self, item_id: str) -> WarehouseStockItemDTO | None:
        """
        Retrieves a warehouse stock item by its ID.
        """
        logger.debug(f"[GET_BY_ID] Starting retrieval operation for warehouse stock item ID: {item_id}")
        stock_item = WarehouseStockItemDAO.get_by_id(item_id)
        if stock_item:
            logger.debug(
                f"[GET_BY_ID] Successfully retrieved stock item - Item ID: {stock_item.item_id} | Status: {stock_item.status} | Warehouse: {stock_item.warehouse_id}")
            return WarehouseStockItemMapper.to_dto(stock_item)
        logger.debug(f"[GET_BY_ID] No warehouse stock item found in database with ID: {item_id}")
        return None

    def get_all(self) -> list[WarehouseStockItemDTO]:
        """
        Retrieves all warehouse stock items.
        """
        logger.debug(f"[GET_ALL] Beginning retrieval of all warehouse stock items")
        stock_item_list = WarehouseStockItemDAO.get_all()
        logger.debug(
            f"[GET_ALL] Retrieved {len(stock_item_list)} stock items | Sold Items: {sum(1 for item in stock_item_list if item.sold)}")
        return WarehouseStockItemMapper.to_dto_list(stock_item_list)

    def get_by_warehouse_id(self, warehouse_id: str) -> list[WarehouseStockItemDTO]:
        """
        Retrieves all warehouse stock items for a given warehouse.
        """
        logger.debug(f"[GET_BY_WAREHOUSE] Beginning retrieval of all stock items for Warehouse ID: {warehouse_id}")
        stock_item_list = WarehouseStockItemDAO.get_by_warehouse_id(warehouse_id)
        logger.debug(
            f"[GET_BY_WAREHOUSE] Retrieved {len(stock_item_list)} stock items | Sold Items: {sum(1 for item in stock_item_list if item.sold)}")
        return WarehouseStockItemMapper.to_dto_list(stock_item_list)

    def get_by_item_id(self, item_id: str) -> list[WarehouseStockItemDTO]:
        """
        Retrieves all warehouse stock items for a given abstract product.
        """
        logger.debug(f"[GET_BY_ITEM] Beginning retrieval of all stock items for Item ID: {item_id}")
        stock_item_list = WarehouseStockItemDAO.get_by_item_id(item_id)
        logger.debug(
            f"[GET_BY_ITEM] Retrieved {len(stock_item_list)} stock items | Sold Items: {sum(1 for item in stock_item_list if item.sold)}")
        return WarehouseStockItemMapper.to_dto_list(stock_item_list)

    def get_by_barcode(self, barcode: str) -> WarehouseStockItemDTO | None:
        """
        Retrieves a warehouse stock item by its barcode.
        """
        logger.debug(f"[GET_BY_BARCODE] Starting retrieval operation for barcode: {barcode}")
        stock_item = WarehouseStockItemDAO.get_by_barcode(barcode)
        if stock_item:
            logger.debug(
                f"[GET_BY_BARCODE] Successfully retrieved stock item - ID: {stock_item.warehouse_stock_item_id} | Item ID: {stock_item.item_id} | Warehouse: {stock_item.warehouse_id}")
            return WarehouseStockItemMapper.to_dto(stock_item)
        logger.debug(f"[GET_BY_BARCODE] No warehouse stock item found in database with barcode: {barcode}")
        return None

    def get_by_identification_code(self, identification_code: str) -> WarehouseStockItemDTO | None:
        """
        Retrieves a warehouse stock item by its identification code.
        """
        logger.debug(f"[GET_BY_CODE] Starting retrieval operation for identification code: {identification_code}")
        stock_item = WarehouseStockItemDAO.get_by_identification_code(identification_code)
        if stock_item:
            logger.debug(
                f"[GET_BY_CODE] Successfully retrieved stock item - ID: {stock_item.warehouse_stock_item_id} | Item ID: {stock_item.item_id} | Warehouse: {stock_item.warehouse_id}")
            return WarehouseStockItemMapper.to_dto(stock_item)
        logger.debug(f"[GET_BY_CODE] No warehouse stock item found in database with identification code: {identification_code}")
        return None

    def add(self, stock_item_dto: WarehouseStockItemDTO) -> WarehouseStockItemDTO:
        """
        Adds a new Warehouse Stock Item.
        """
        logger.debug(
            f"[ADD_STOCK_ITEM] Initiating creation of new stock item - Item ID: {stock_item_dto.item_id} | Warehouse: {stock_item_dto.warehouse_id}")
        stock_item = WarehouseStockItemMapper.to_model(stock_item_dto)
        logger.debug(
            f"[ADD_STOCK_ITEM] Successfully mapped DTO to model - Barcode: {stock_item_dto.bar_code} | Identification Code: {stock_item_dto.identification_code}")
        stock_item_dao = WarehouseStockItemDAO.save(stock_item)
        logger.debug(
            f"[ADD_STOCK_ITEM] Stock item successfully persisted in database with ID: {stock_item_dao.warehouse_stock_item_id} | Status: {stock_item_dao.status}")
        return WarehouseStockItemMapper.to_dto(stock_item_dao)

    def update(self, stock_item_dto: WarehouseStockItemDTO) -> WarehouseStockItemDTO:
        """
        Updates an existing Warehouse Stock Item.
        """
        logger.debug(
            f"[UPDATE_STOCK_ITEM] Starting update process for stock item ID: {stock_item_dto.warehouse_stock_item_id} | Warehouse ID: {stock_item_dto.warehouse_id} | Item ID: {stock_item_dto.item_id}")
        stock_item = WarehouseStockItemMapper.to_model(stock_item_dto)
        logger.debug(
            f"[UPDATE_STOCK_ITEM] Successfully mapped DTO to model - Status: {stock_item_dto.status} | Sold: {stock_item_dto.sold}")
        stock_item_dao = WarehouseStockItemDAO.update(stock_item)
        logger.debug(
            f"[UPDATE_STOCK_ITEM] Database update completed successfully for stock item ID: {stock_item_dto.warehouse_stock_item_id} | New Status: {stock_item_dao.status}")
        return WarehouseStockItemMapper.to_dto(stock_item_dao)

    def delete(self, item_id: str) -> bool:
        """
        Deletes a Warehouse Stock Item by its ID.
        """
        logger.debug(f"[DELETE_STOCK_ITEM] Starting deletion process for stock item ID: {item_id}")
        result = WarehouseStockItemDAO.delete(item_id)
        logger.debug(f"[DELETE_STOCK_ITEM] Deletion operation completed - Success: {result} | Stock Item ID: {item_id}")
        return result