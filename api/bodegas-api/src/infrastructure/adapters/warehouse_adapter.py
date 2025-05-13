import logging

from ..dao.warehouse_dao import WarehouseDAO
from ..mapper.warehouse_mapper import WarehouseMapper
from ...domain.entities.warehouse_dto import WarehouseDTO
from ...domain.repositories.warehouse_repository import WarehouseRepository

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class WarehouseAdapter(WarehouseRepository):
    """
    Adapter for WarehouseRepository to interact with WarehouseDAO and WarehouseMapper.
    """

    def get_by_id(self, warehouse_id: str) -> WarehouseDTO | None:
        """
        Retrieves a warehouse by its ID.
        """
        logger.debug(f"[GET_BY_ID] Starting retrieval operation for warehouse ID: {warehouse_id}")
        warehouse = WarehouseDAO.get_by_id(warehouse_id)
        if warehouse:
            logger.debug(
                f"[GET_BY_ID] Successfully retrieved warehouse - Name: {warehouse.name} | Status: {warehouse.status} | Administrator: {warehouse.administrator_id}")
            return WarehouseMapper.to_dto(warehouse)
        logger.debug(f"[GET_BY_ID] No warehouse found in database with ID: {warehouse_id}")
        return None

    def get_all(self) -> list[WarehouseDTO]:
        """
        Retrieves all warehouses.
        """
        logger.debug(f"[GET_ALL] Beginning retrieval of all warehouses")
        warehouse_list = WarehouseDAO.get_all()
        logger.debug(
            f"[GET_ALL] Retrieved {len(warehouse_list)} warehouses | Active Warehouses: {sum(1 for warehouse in warehouse_list if warehouse.status == 'active')}")
        return WarehouseMapper.to_dto_list(warehouse_list)

    def get_by_administrator_id(self, administrator_id: str) -> list[WarehouseDTO]:
        """
        Retrieves all warehouses for a given administrator.
        """
        logger.debug(f"[GET_BY_ADMINISTRATOR] Beginning retrieval of all warehouses for Administrator ID: {administrator_id}")
        warehouse_list = WarehouseDAO.get_by_administrator_id(administrator_id)
        logger.debug(
            f"[GET_BY_ADMINISTRATOR] Retrieved {len(warehouse_list)} warehouses | Active Warehouses: {sum(1 for warehouse in warehouse_list if warehouse.status == 'active')}")
        return WarehouseMapper.to_dto_list(warehouse_list)

    def add(self, warehouse_dto: WarehouseDTO) -> WarehouseDTO:
        """
        Adds a new Warehouse.
        """
        logger.debug(
            f"[ADD_WAREHOUSE] Initiating creation of new warehouse - Name: {warehouse_dto.name} | Administrator: {warehouse_dto.administrator_id}")
        warehouse = WarehouseMapper.to_model(warehouse_dto)
        logger.debug(
            f"[ADD_WAREHOUSE] Successfully mapped DTO to model - Location: {warehouse_dto.location} | Description: {warehouse_dto.description}")
        warehouse_dao = WarehouseDAO.save(warehouse)
        logger.debug(
            f"[ADD_WAREHOUSE] Warehouse successfully persisted in database with ID: {warehouse_dao.id} | Status: {warehouse_dao.status}")
        return WarehouseMapper.to_dto(warehouse_dao)

    def update(self, warehouse_dto: WarehouseDTO) -> WarehouseDTO:
        """
        Updates an existing Warehouse.
        """
        logger.debug(
            f"[UPDATE_WAREHOUSE] Starting update process for warehouse ID: {warehouse_dto.id} | Administrator ID: {warehouse_dto.administrator_id} | Name: {warehouse_dto.name}")
        warehouse = WarehouseMapper.to_model(warehouse_dto)
        logger.debug(
            f"[UPDATE_WAREHOUSE] Successfully mapped DTO to model - Status: {warehouse_dto.status} | Location: {warehouse_dto.location}")
        warehouse_dao = WarehouseDAO.update(warehouse)
        logger.debug(
            f"[UPDATE_WAREHOUSE] Database update completed successfully for warehouse ID: {warehouse_dto.id} | New Status: {warehouse_dao.status}")
        return WarehouseMapper.to_dto(warehouse_dao)

    def delete(self, warehouse_id: str) -> bool:
        """
        Deletes a Warehouse by its ID.
        """
        logger.debug(f"[DELETE_WAREHOUSE] Starting deletion process for warehouse ID: {warehouse_id}")
        result = WarehouseDAO.delete(warehouse_id)
        logger.debug(f"[DELETE_WAREHOUSE] Deletion operation completed - Success: {result} | Warehouse ID: {warehouse_id}")
        return result