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


class GetWarehouseById:
    """
    Use case for retrieving a warehouse by its ID.
    """

    def __init__(self, warehouse_repository: WarehouseRepository):
        """
        Initialize the use case with a warehouse repository.
        
        :param warehouse_repository: Repository for warehouse operations
        """
        self.warehouse_repository = warehouse_repository

    def execute(self, warehouse_id: str) -> WarehouseDTO:
        """
        Execute the use case to retrieve a warehouse by its ID.
        
        :param warehouse_id: ID of the warehouse to retrieve
        :return: Retrieved warehouse DTO
        :raises ResourceNotFoundError: If the warehouse doesn't exist
        """
        logger.debug(f"[GET_WAREHOUSE_BY_ID] Starting retrieval of warehouse with ID: {warehouse_id}")
        
        # Get the warehouse using the repository
        warehouse = self.warehouse_repository.get_by_id(warehouse_id)
        
        # Check if the warehouse exists
        if not warehouse:
            logger.error(f"[GET_WAREHOUSE_BY_ID] Warehouse with ID {warehouse_id} not found")
            raise ResourceNotFoundError
        
        logger.debug(f"[GET_WAREHOUSE_BY_ID] Successfully retrieved warehouse with ID: {warehouse.warehouse_id}")
        return warehouse