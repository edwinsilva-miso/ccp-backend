from datetime import datetime, timezone

from sqlalchemy.orm import joinedload

from ..database.declarative_base import Session
from ..model.orders_model import OrderModel


class OrderDAO:
    """
    Data Access Object for OrderModel.
    """

    @classmethod
    def find_all(cls) -> list[OrderModel]:
        """
        Get all orders.
        :return: List of OrderModel.
        """
        session = Session()
        orders = session.query(OrderModel).order_by(OrderModel.order_date.desc()).all()
        session.close()
        return orders

    @classmethod
    def find_by_client_id(cls, client_id: str) -> list[OrderModel]:
        """
        Get order by Client ID.
        :param client_id: ID of the client to find.
        :return: OrderModel if found, None otherwise.
        """
        with Session() as session:
            # Load order and relationships in a single query
            order = session.query(OrderModel) \
                .options(
                joinedload(OrderModel.order_items),
                joinedload(OrderModel.order_history)
            ) \
                .filter(OrderModel.client_id == client_id) \
                .first()
            return order

    @classmethod
    def get_by_id(cls, order_id: str) -> OrderModel | None:
        """
        Get order by ID.
        :param order_id: ID of the order to find.
        :return: OrderModel if found, None otherwise.
        """
        with Session() as session:
            # Load order and relationships in a single query
            order = session.query(OrderModel) \
                .options(
                joinedload(OrderModel.order_items),
                joinedload(OrderModel.order_history)
            ) \
                .filter(OrderModel.id == order_id) \
                .first()
            return order

    @classmethod
    def save(cls, order: OrderModel) -> str:
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
        return order.id

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
