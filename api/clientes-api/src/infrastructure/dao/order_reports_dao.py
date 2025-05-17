from ..database.declarative_base import Session
from ..model.order_reports_model import OrderReportsModel

class OrderReportsDAO:
    """
    OrderReportsDAO is a data access object for the OrderReportsModel.
    It provides methods to interact with the order reports in the database.
    """

    @classmethod
    def save(cls, order_report: OrderReportsModel) -> OrderReportsModel:
        """
        Save a new order report to the database.
        :param order_report: OrderReportsModel to save.
        :return: ID of the saved order report.
        """
        session = Session()
        session.add(order_report)
        session.commit()
        session.refresh(order_report)
        session.close()
        return order_report

    @classmethod
    def get_by_user_id(cls, user_id: str) -> list[OrderReportsModel]:
        """
        Get all order reports by user ID.
        :param user_id: ID of the user to find order reports for.
        :return: List of OrderReportsModel if found.
        """
        session = Session()
        order_reports = session.query(OrderReportsModel).filter(OrderReportsModel.user_id == user_id).all()
        session.close()
        return order_reports