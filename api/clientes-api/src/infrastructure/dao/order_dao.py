from datetime import datetime, timezone

from ..database.declarative_base import Session
from ..model.order_model import OrderModel


class OrderDAO:

    @classmethod
    def find_by_client_id(cls, client_id: str) -> list[OrderModel]:
        """
        Find all orders by client ID.
        :param client_id: ID of the client to find orders for.
        :return: List of OrderModel if found.
        """
        session = Session()
        orders = session.query(OrderModel).filter(OrderModel.client_id == client_id).all()
        session.close()
        return orders

    @classmethod
    def get_by_id(cls, order_id: str) -> OrderModel | None:
        """
        Get order by ID.
        :param order_id: ID of the order to find.
        :return: OrderModel if found, None otherwise.
        """
        session = Session()
        order = session.query(OrderModel).filter(OrderModel.id == order_id).first()
        session.close()
        return order

    @classmethod
    def save(cls, order: OrderModel) -> OrderModel:
        """
        Save a new order to the database.
        :param order: OrderModel to save.
        :return: ID of the saved order.
        """
        session = Session()
        order.created_at = datetime.now(timezone.utc)
        session.add(order)
        session.commit()
        session.refresh(order)
        session.close()
        return order

    @classmethod
    def update(cls, order: OrderModel) -> OrderModel:
        """Update an existing order"""
        session = Session()
        order.updated_at = datetime.now(timezone.utc)
        session.merge(order)
        session.commit()
        session.refresh(order)
        session.close()
        return order
