import logging

from flask import Blueprint, jsonify

from ..decorator.token_decorator import token_required
from ...application.list_orders import ListsOrders
from ...application.get_order_by_id import GetOrderById
from ...infrastructure.adapters.order_adapter import OrdersAdapter

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)
logger = logging.getLogger(__name__)

orders_adapter = OrdersAdapter()

orders_blueprint = Blueprint('orders', __name__, url_prefix='/api/v1/orders')


@orders_blueprint.route('', methods=['GET'])
@token_required(['DIRECTIVO'])
def list_orders():
    """
    Endpoint to list all orders for a given client ID.
    """
    logger.debug("Starting order listing process...")
    use_case = ListsOrders(orders_adapter)
    orders = use_case.execute()
    return jsonify([order.to_dict() for order in orders]), 200

@orders_blueprint.route('/<order_id>', methods=['GET'])
@token_required(['DIRECTIVO', 'CLIENTE'])
def get_order_by_id(order_id):
    """
    Endpoint to get an order by its ID.
    """
    logger.debug(f"Getting order with ID: {order_id}")
    use_case = GetOrderById(orders_adapter)
    order = use_case.execute(order_id)
    return jsonify(order.to_dict()), 200
