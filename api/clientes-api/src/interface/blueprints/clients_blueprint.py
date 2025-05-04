import logging

from flask import Blueprint, jsonify, request

from ..decorator.token_decorator import token_required
from ...application.create_order import CreateOrder
from ...application.list_orders  import ListOrders
from ...application.errors.errors import ValidationApiError
from ...infrastructure.adapters.orders_adapter import OrdersAdapter
from ...infrastructure.adapters.payments_adapter import PaymentsAdapter
from ...infrastructure.messaging.rabbitmq_messaging_port_adapter import RabbitMQMessagingPortAdapter

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)
logger = logging.getLogger(__name__)

orders_adapter = OrdersAdapter()
payments_adapter = PaymentsAdapter()
messaging_port_adapter = RabbitMQMessagingPortAdapter()

clients_blueprint = Blueprint('clients', __name__, url_prefix='/api/v1/clients')


@clients_blueprint.route('/orders', methods=['POST'])
@token_required(['CLIENTE'])
def create_order():
    """
    Endpoint to create a new order.
    """
    data = request.get_json()
    if not data:
        logger.error("No data provided in request.")
        raise ValidationApiError

    use_case = CreateOrder(orders_adapter, payments_adapter, messaging_port_adapter)
    response, status = use_case.execute(data)
    return jsonify(response), status

@clients_blueprint.route('/orders', methods=['GET'])
@token_required(['CLIENTE'])
def list_orders():
    """
    Endpoint to list all orders for a given client ID.
    """
    client_id = request.args.get('clientId')
    if not client_id:
        logger.error("Missing client ID in request.")
        return jsonify({'msg': 'Client ID is required.'}), 400

    logger.debug("Starting order listing process...")
    use_case = ListOrders(orders_adapter)
    orders = use_case.execute(client_id)
    return jsonify([order.to_dict() for order in orders]), 200
