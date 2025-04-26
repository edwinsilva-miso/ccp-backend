import logging

from flask import Blueprint, jsonify, request

from ...application.create_purchase import CreatePurchase
from ...application.errors.errors import ValidationApiError
from ...infrastructure.adapters.orders_adapter import OrdersAdapter
from ...infrastructure.adapters.payments_adapter import PaymentsAdapter

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)
logger = logging.getLogger(__name__)

orders_adapter = OrdersAdapter()
payments_adapter = PaymentsAdapter()

orders_blueprint = Blueprint('orders', __name__, url_prefix='/api/v1/orders')


@orders_blueprint.route('/', methods=['POST'])
def create_order():
    """
    Endpoint to create a new order.
    """
    data = request.get_json()
    if not data:
        logger.error("No data provided in request.")
        raise ValidationApiError

    use_case = CreatePurchase(orders_adapter, payments_adapter)
    response = use_case.execute(data)
    return jsonify(response), 201
