from abc import ABC, abstractmethod

from ..entities.warehouse_dto import WarehouseDTO


class WarehouseRepository(ABC):
    """
    Port defining the interface for Warehouse repository.
    """

    @abstractmethod
    def get_by_id(self, warehouse_id: str) -> WarehouseDTO:
        """
        Retrieves a warehouse by its ID.
        :param warehouse_id: ID of the warehouse
        :return: WarehouseDTO object
        """
        pass

    @abstractmethod
    def get_all(self) -> list[WarehouseDTO]:
        """
        Retrieves all warehouses.
        :return: List of WarehouseDTO objects
        """
        pass

    @abstractmethod
    def get_by_administrator_id(self, administrator_id: str) -> list[WarehouseDTO]:
        """
        Retrieves all warehouses for a given administrator.
        :param administrator_id: ID of the administrator
        :return: List of WarehouseDTO objects
        """
        pass

    @abstractmethod
    def add(self, warehouse_dto: WarehouseDTO) -> WarehouseDTO:
        """
        Adds a new Warehouse.
        :param warehouse_dto: WarehouseDTO object to add
        :return: WarehouseDTO object
        """
        pass

    @abstractmethod
    def update(self, warehouse_dto: WarehouseDTO) -> WarehouseDTO:
        """
        Updates an existing Warehouse.
        :param warehouse_dto: WarehouseDTO object to update
        :return: WarehouseDTO object
        """
        pass

    @abstractmethod
    def delete(self, warehouse_id: str) -> bool:
        """
        Deletes a Warehouse by its ID.
        :param warehouse_id: ID of the warehouse to delete
        :return: True if deleted successfully, False otherwise
        """
        pass