import logging

from ...application.errors.errors import ResourceNotFoundError
from ...domain.entities.warehouse_dto import WarehouseDTO
from ...domain.repositories.warehouse_repository import WarehouseRepository

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class UpdateWarehouse:
    """
    Use case for updating an existing warehouse.
    """

    def __init__(self, warehouse_repository: WarehouseRepository):
        """
        Initialize the use case with a warehouse repository.
        
        :param warehouse_repository: Repository for warehouse operations
        """
        self.warehouse_repository = warehouse_repository

    def execute(self, warehouse_dto: WarehouseDTO) -> WarehouseDTO:
        """
        Execute the use case to update an existing warehouse.
        
        :param warehouse_dto: DTO containing updated warehouse data
        :return: Updated warehouse DTO
        :raises ResourceNotFoundError: If the warehouse doesn't exist
        """
        logger.debug(f"[UPDATE_WAREHOUSE] Starting update of warehouse with ID: {warehouse_dto.warehouse_id}")
        
        # Check if the warehouse exists
        existing_warehouse = self.warehouse_repository.get_by_id(warehouse_dto.warehouse_id)
        if not existing_warehouse:
            logger.error(f"[UPDATE_WAREHOUSE] Warehouse with ID {warehouse_dto.warehouse_id} not found")
            raise ResourceNotFoundError
        
        # Update the warehouse using the repository
        updated_warehouse = self.warehouse_repository.update(warehouse_dto)
        
        logger.debug(f"[UPDATE_WAREHOUSE] Successfully updated warehouse with ID: {updated_warehouse.warehouse_id}")
        return updated_warehouse