from ..database.declarative_base import Session
from ..model.warehouse_stock_item_model import WarehouseStockItemModel


class WarehouseStockItemDAO:
    """
    Data Access Object (DAO) for WarehouseStockItemModel.
    Provides an interface to interact with the database.
    """

    @classmethod
    def save(cls, stock_item: WarehouseStockItemModel) -> WarehouseStockItemModel:
        """
        Create a new warehouse stock item record in the database.
        :param stock_item: WarehouseStockItemModel to save.
        :return: The saved WarehouseStockItemModel with its ID.
        """
        session = Session()
        session.add(stock_item)
        session.commit()
        session.refresh(stock_item)
        session.close()
        return stock_item

    @classmethod
    def update(cls, stock_item: WarehouseStockItemModel) -> WarehouseStockItemModel:
        """
        Update an existing warehouse stock item record in the database.
        :param stock_item: WarehouseStockItemModel to update.
        :return: The updated WarehouseStockItemModel.
        """
        session = Session()
        merged_item = session.merge(stock_item)
        session.commit()
        session.refresh(merged_item)
        session.close()
        return merged_item

    @classmethod
    def delete(cls, item_id: str) -> bool:
        """
        Delete a warehouse stock item record from the database.
        :param item_id: ID of the warehouse stock item to delete.
        :return: True if deleted successfully, False otherwise.
        """
        session = Session()
        stock_item = session.query(WarehouseStockItemModel).filter(WarehouseStockItemModel.id == item_id).first()
        if stock_item:
            session.delete(stock_item)
            session.commit()
            session.close()
            return True
        session.close()
        return False

    @classmethod
    def get_by_id(cls, item_id: str) -> WarehouseStockItemModel | None:
        """
        Get a warehouse stock item record by ID.
        :param item_id: ID of the warehouse stock item to retrieve.
        :return: WarehouseStockItemModel if found, None otherwise.
        """
        session = Session()
        stock_item = session.query(WarehouseStockItemModel).filter(WarehouseStockItemModel.id == item_id).first()
        session.close()
        return stock_item

    @classmethod
    def get_all(cls) -> list[WarehouseStockItemModel]:
        """
        Get all warehouse stock item records.
        :return: List of all WarehouseStockItemModel.
        """
        session = Session()
        stock_items = session.query(WarehouseStockItemModel).all()
        session.close()
        return stock_items

    @classmethod
    def get_by_warehouse_id(cls, warehouse_id: str) -> list[WarehouseStockItemModel]:
        """
        Get all warehouse stock item records by warehouse ID.
        :param warehouse_id: ID of the warehouse to retrieve stock items for.
        :return: List of WarehouseStockItemModel with the specified warehouse ID.
        """
        session = Session()
        stock_items = session.query(WarehouseStockItemModel).filter(WarehouseStockItemModel.warehouse_id == warehouse_id).all()
        session.close()
        return stock_items

    @classmethod
    def get_by_item_id(cls, item_id: str) -> list[WarehouseStockItemModel]:
        """
        Get all warehouse stock item records by item ID.
        :param item_id: ID of the abstract product to retrieve stock items for.
        :return: List of WarehouseStockItemModel with the specified item ID.
        """
        session = Session()
        stock_items = session.query(WarehouseStockItemModel).filter(WarehouseStockItemModel.item_id == item_id).all()
        session.close()
        return stock_items

    @classmethod
    def get_by_barcode(cls, barcode: str) -> WarehouseStockItemModel | None:
        """
        Get a warehouse stock item record by barcode.
        :param barcode: Barcode of the warehouse stock item to retrieve.
        :return: WarehouseStockItemModel if found, None otherwise.
        """
        session = Session()
        stock_item = session.query(WarehouseStockItemModel).filter(WarehouseStockItemModel.barcode == barcode).first()
        session.close()
        return stock_item

    @classmethod
    def get_by_identification_code(cls, identification_code: str) -> WarehouseStockItemModel | None:
        """
        Get a warehouse stock item record by identification code.
        :param identification_code: Identification code of the warehouse stock item to retrieve.
        :return: WarehouseStockItemModel if found, None otherwise.
        """
        session = Session()
        stock_item = session.query(WarehouseStockItemModel).filter(WarehouseStockItemModel.identification_code == identification_code).first()
        session.close()
        return stock_item