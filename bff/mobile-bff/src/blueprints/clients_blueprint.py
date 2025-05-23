import functools
import logging

from flask import Blueprint, jsonify, request

from ..adapters.clients_adapter import ClientsAdapter
from ..utils.commons import token_required

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

orders_blueprint = Blueprint('orders', __name__, url_prefix='/bff/v1/mobile/clients/orders')


@orders_blueprint.route('/', methods=['POST'])
@token_required
def create_order(jwt):
    """
    Create a new order.
    :param jwt: JWT token for authorization.
    :return: The created order data
    """
    logging.debug("Received request to create a new order.")
    logging.debug("Creating order in BFF Mobile.")
    salesman_id = request.headers.get('salesman-id')
    adapter = ClientsAdapter()
    order_data = request.get_json()
    return adapter.create_order(jwt, order_data, salesman_id)

@orders_blueprint.route('/', methods=['GET'])
@token_required
def list_orders(jwt):
    """
    List orders for a specific client.
    :param jwt: JWT token for authorization.
    :return: The list of orders
    """
    logging.debug("Received request to list orders.")
    logging.debug("Listing orders in BFF Mobile.")
    adapter = ClientsAdapter()
    client_id = request.args.get('clientId')
    return adapter.lists_orders(jwt, client_id)

@orders_blueprint.route('/<order_id>', methods=['GET'])
@token_required
def get_order(jwt, order_id):
    """
    Get details of a specific order.
    :param jwt: JWT token for authorization.
    :param order_id: The ID of the order to retrieve.
    :return: The order data
    """
    logging.debug("Received request to get order details.")
    logging.debug("Getting order details in BFF Mobile.")
    adapter = ClientsAdapter()
    return adapter.get_order_by_id(jwt, order_id)

@orders_blueprint.route('/salesman/<salesman_id>', methods=['GET'])
@token_required
def list_orders_by_salesman(jwt, salesman_id):
    """
    List orders for a specific salesman.
    :param jwt: JWT token for authorization.
    :param salesman_id: The ID of the salesman to list orders for.
    :return: The list of orders
    """
    logging.debug("Received request to list orders by salesman.")
    logging.debug("Listing orders by salesman in BFF Mobile.")
    adapter = ClientsAdapter()
    return adapter.get_orders_by_salesman_id(jwt, salesman_id)