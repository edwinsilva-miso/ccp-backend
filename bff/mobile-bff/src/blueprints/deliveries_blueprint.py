import logging
from flask import Blueprint, request

from ..adapters.deliveries_adapter import DeliveriesAdapter
from ..utils.commons import validate_token

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

deliveries_blueprint = Blueprint('deliveries', __name__, url_prefix='/bff/v1/mobile/deliveries')


# Customer endpoints
@deliveries_blueprint.route('/customers/<uuid:customer_id>', methods=['GET'])
@validate_token
def get_customer_deliveries(customer_id, jwt):
    """Get all deliveries for a customer."""
    logger.debug(f"received request to get deliveries for customer with id: {customer_id}")
    adapter = DeliveriesAdapter()
    return adapter.get_customer_deliveries(jwt, customer_id)


@deliveries_blueprint.route('/customers/<uuid:customer_id>/deliveries/<uuid:delivery_id>', methods=['GET'])
@validate_token
def get_delivery_for_customer(customer_id, delivery_id, jwt):
    """Get a specific delivery for a customer."""
    logger.debug(f"received request to get delivery with id: {delivery_id} for customer: {customer_id}")
    adapter = DeliveriesAdapter()
    return adapter.get_delivery_for_customer(jwt, delivery_id, customer_id)


# Seller endpoints
@deliveries_blueprint.route('/sellers/deliveries', methods=['POST'])
@validate_token
def create_delivery(jwt):
    """Create a new delivery."""
    logger.debug("received request to create a new delivery")
    delivery_data = request.get_json()
    adapter = DeliveriesAdapter()
    return adapter.create_delivery(jwt, delivery_data)


@deliveries_blueprint.route('/sellers/<uuid:seller_id>/deliveries', methods=['GET'])
@validate_token
def get_seller_deliveries(seller_id, jwt):
    """Get all deliveries for a seller."""
    logger.debug(f"received request to get deliveries for seller with id: {seller_id}")
    adapter = DeliveriesAdapter()
    return adapter.get_seller_deliveries(jwt, seller_id)


@deliveries_blueprint.route('/sellers/<uuid:seller_id>/deliveries/<uuid:delivery_id>', methods=['GET'])
@validate_token
def get_delivery_for_seller(seller_id, delivery_id, jwt):
    """Get a specific delivery for a seller."""
    logger.debug(f"received request to get delivery with id: {delivery_id} for seller: {seller_id}")
    adapter = DeliveriesAdapter()
    return adapter.get_delivery_for_seller(jwt, delivery_id, seller_id)


@deliveries_blueprint.route('/sellers/deliveries/<uuid:delivery_id>', methods=['PUT'])
@validate_token
def update_delivery(delivery_id, jwt):
    """Update a delivery."""
    logger.debug(f"received request to update delivery with id: {delivery_id}")
    delivery_data = request.get_json()
    adapter = DeliveriesAdapter()
    return adapter.update_delivery(jwt, delivery_id, delivery_data)


@deliveries_blueprint.route('/sellers/<uuid:seller_id>/deliveries/<uuid:delivery_id>', methods=['DELETE'])
@validate_token
def delete_delivery(seller_id, delivery_id, jwt):
    """Delete a delivery."""
    logger.debug(f"received request to delete delivery with id: {delivery_id} for seller: {seller_id}")
    adapter = DeliveriesAdapter()
    return adapter.delete_delivery(jwt, delivery_id, seller_id)


@deliveries_blueprint.route('/sellers/deliveries/<uuid:delivery_id>/status', methods=['POST'])
@validate_token
def add_status_update(delivery_id, jwt):
    """Add a status update to a delivery."""
    logger.debug(f"received request to add status update to delivery with id: {delivery_id}")
    status_data = request.get_json()
    adapter = DeliveriesAdapter()
    return adapter.add_status_update(jwt, delivery_id, status_data)


@deliveries_blueprint.route('/sellers/status/<uuid:status_update_id>', methods=['PUT'])
@validate_token
def update_status_update(status_update_id, jwt):
    """Update a status update."""
    logger.debug(f"received request to update status update with id: {status_update_id}")
    status_data = request.get_json()
    adapter = DeliveriesAdapter()
    return adapter.update_status_update(jwt, status_update_id, status_data)


@deliveries_blueprint.route('/sellers/<uuid:seller_id>/status/<uuid:status_update_id>', methods=['DELETE'])
@validate_token
def delete_status_update(seller_id, status_update_id, jwt):
    """Delete a status update."""
    logger.debug(f"received request to delete status update with id: {status_update_id} for seller: {seller_id}")
    adapter = DeliveriesAdapter()
    return adapter.delete_status_update(jwt, status_update_id, seller_id)
