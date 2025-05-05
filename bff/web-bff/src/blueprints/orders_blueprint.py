import logging
import functools

from flask import Blueprint, request, jsonify

from ..adapters.orders_adapter import OrdersAdapter

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

orders_blueprint = Blueprint('orders', __name__, url_prefix='/bff/v1/web/orders')

def token_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            logger.error("Missing Authorization header.")
            return jsonify({'msg': 'Unauthorized'}), 401

        jwt = token.split('Bearer ')[-1] if 'Bearer ' in token else token
        kwargs['jwt'] = jwt
        return f(*args, **kwargs)

    return decorated_function

@orders_blueprint.route('', methods=['GET'])
@token_required
def get_all_orders(jwt):
    logger.debug("Received request to get all orders.")
    logger.debug("Retrieving all orders from BFF Web.")
    adapter = OrdersAdapter()
    return adapter.list_orders(jwt)

@orders_blueprint.route('/<order_id>', methods=['GET'])
@token_required
def get_order_by_id(order_id, jwt):
    logger.debug(f"Received request to get order with ID: {order_id}")
    logger.debug("Retrieving order by ID from BFF Web.")
    adapter = OrdersAdapter()
    return adapter.get_order_by_id(jwt, order_id)