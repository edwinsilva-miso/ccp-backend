from ..database.declarative_base import Session
from ..model.warehouse_model import WarehouseModel


class WarehouseDAO:
    """
    Data Access Object (DAO) for WarehouseModel.
    Provides an interface to interact with the database.
    """

    @classmethod
    def save(cls, warehouse: WarehouseModel) -> WarehouseModel:
        """
        Create a new warehouse record in the database.
        :param warehouse: WarehouseModel to save.
        :return: The saved WarehouseModel with its ID.
        """
        session = Session()
        session.add(warehouse)
        session.commit()
        session.refresh(warehouse)
        session.close()
        return warehouse

    @classmethod
    def update(cls, warehouse: WarehouseModel) -> WarehouseModel:
        """
        Update an existing warehouse record in the database.
        :param warehouse: WarehouseModel to update.
        :return: The updated WarehouseModel.
        """
        session = Session()
        merged_warehouse = session.merge(warehouse)
        session.commit()
        session.refresh(merged_warehouse)
        session.close()
        return merged_warehouse

    @classmethod
    def delete(cls, warehouse_id: str) -> bool:
        """
        Delete a warehouse record from the database.
        :param warehouse_id: ID of the warehouse to delete.
        :return: True if deleted successfully, False otherwise.
        """
        session = Session()
        warehouse = session.query(WarehouseModel).filter(WarehouseModel.id == warehouse_id).first()
        if warehouse:
            session.delete(warehouse)
            session.commit()
            session.close()
            return True
        session.close()
        return False

    @classmethod
    def get_by_id(cls, warehouse_id: str) -> WarehouseModel | None:
        """
        Get a warehouse record by ID.
        :param warehouse_id: ID of the warehouse to retrieve.
        :return: WarehouseModel if found, None otherwise.
        """
        session = Session()
        warehouse = session.query(WarehouseModel).filter(WarehouseModel.id == warehouse_id).first()
        session.close()
        return warehouse

    @classmethod
    def get_all(cls) -> list[WarehouseModel]:
        """
        Get all warehouse records.
        :return: List of all WarehouseModel.
        """
        session = Session()
        warehouses = session.query(WarehouseModel).all()
        session.close()
        return warehouses

    @classmethod
    def get_by_administrator_id(cls, administrator_id: str) -> list[WarehouseModel]:
        """
        Get all warehouse records by administrator ID.
        :param administrator_id: ID of the administrator to retrieve warehouses for.
        :return: List of WarehouseModel with the specified administrator ID.
        """
        session = Session()
        warehouses = session.query(WarehouseModel).filter(WarehouseModel.administrator_id == administrator_id).all()
        session.close()
        return warehouses