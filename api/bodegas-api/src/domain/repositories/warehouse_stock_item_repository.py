from abc import ABC, abstractmethod

from ..entities.warehouse_stock_item_dto import WarehouseStockItemDTO


class WarehouseStockItemRepository(ABC):
    """
    Port defining the interface for Warehouse Stock Item repository.
    """

    @abstractmethod
    def get_by_id(self, item_id: str) -> WarehouseStockItemDTO:
        """
        Retrieves a warehouse stock item by its ID.
        :param item_id: ID of the warehouse stock item
        :return: WarehouseStockItemDTO object
        """
        pass

    @abstractmethod
    def get_all(self) -> list[WarehouseStockItemDTO]:
        """
        Retrieves all warehouse stock items.
        :return: List of WarehouseStockItemDTO objects
        """
        pass

    @abstractmethod
    def get_by_warehouse_id(self, warehouse_id: str) -> list[WarehouseStockItemDTO]:
        """
        Retrieves all warehouse stock items for a given warehouse.
        :param warehouse_id: ID of the warehouse
        :return: List of WarehouseStockItemDTO objects
        """
        pass

    @abstractmethod
    def get_by_item_id(self, item_id: str) -> list[WarehouseStockItemDTO]:
        """
        Retrieves all warehouse stock items for a given abstract product.
        :param item_id: ID of the abstract product
        :return: List of WarehouseStockItemDTO objects
        """
        pass

    @abstractmethod
    def get_by_barcode(self, barcode: str) -> WarehouseStockItemDTO:
        """
        Retrieves a warehouse stock item by its barcode.
        :param barcode: Barcode of the warehouse stock item
        :return: WarehouseStockItemDTO object
        """
        pass

    @abstractmethod
    def get_by_identification_code(self, identification_code: str) -> WarehouseStockItemDTO:
        """
        Retrieves a warehouse stock item by its identification code.
        :param identification_code: Identification code of the warehouse stock item
        :return: WarehouseStockItemDTO object
        """
        pass

    @abstractmethod
    def add(self, stock_item_dto: WarehouseStockItemDTO) -> WarehouseStockItemDTO:
        """
        Adds a new Warehouse Stock Item.
        :param stock_item_dto: WarehouseStockItemDTO object to add
        :return: WarehouseStockItemDTO object
        """
        pass

    @abstractmethod
    def update(self, stock_item_dto: WarehouseStockItemDTO) -> WarehouseStockItemDTO:
        """
        Updates an existing Warehouse Stock Item.
        :param stock_item_dto: WarehouseStockItemDTO object to update
        :return: WarehouseStockItemDTO object
        """
        pass

    @abstractmethod
    def delete(self, item_id: str) -> bool:
        """
        Deletes a Warehouse Stock Item by its ID.
        :param item_id: ID of the warehouse stock item to delete
        :return: True if deleted successfully, False otherwise
        """
        pass