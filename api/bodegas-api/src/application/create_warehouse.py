import logging

from ..domain.entities.warehouse_dto import WarehouseDTO
from ..domain.repositories.warehouse_repository import WarehouseRepository

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class CreateWarehouse:
    """
    Use case for creating a new warehouse.
    """

    def __init__(self, warehouse_repository: WarehouseRepository):
        """
        Initialize the use case with a warehouse repository.
        
        :param warehouse_repository: Repository for warehouse operations
        """
        self.warehouse_repository = warehouse_repository

    def execute(self, warehouse_dto: WarehouseDTO) -> WarehouseDTO:
        """
        Execute the use case to create a new warehouse.
        
        :param warehouse_dto: DTO containing warehouse data
        :return: Created warehouse DTO
        """
        logger.debug(f"[CREATE_WAREHOUSE] Starting creation of warehouse: {warehouse_dto.name}")
        
        # Add the warehouse using the repository
        created_warehouse = self.warehouse_repository.add(warehouse_dto)
        
        logger.debug(f"[CREATE_WAREHOUSE] Successfully created warehouse with ID: {created_warehouse.id}")
        return created_warehouse