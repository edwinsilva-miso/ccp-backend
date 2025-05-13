import logging

from flask import Blueprint, request

from ..adapters.warehouse_adapter import WarehouseAdapter
from ..utils.commons import validate_token

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

warehouse_blueprint = Blueprint('warehouse', __name__, url_prefix='/bff/v1/web/warehouses')


@warehouse_blueprint.route('', methods=['POST'])
@validate_token
def create_warehouse(jwt):
    """Create a new warehouse."""
    logger.debug("received request to create a new warehouse")

    warehouse_data = request.get_json()

    adapter = WarehouseAdapter()
    return adapter.create_warehouse(jwt, warehouse_data)


@warehouse_blueprint.route('/<warehouse_id>', methods=['GET'])
@validate_token
def get_warehouse(warehouse_id, jwt):
    """Get a warehouse by ID."""
    logger.debug(f"received request to get warehouse with id: {warehouse_id}")
    adapter = WarehouseAdapter()
    return adapter.get_warehouse_by_id(jwt, warehouse_id)


@warehouse_blueprint.route('', methods=['GET'])
@validate_token
def get_all_warehouses(jwt):
    """Get all warehouses."""
    logger.debug("received request to get all warehouses")
    adapter = WarehouseAdapter()
    return adapter.get_all_warehouses(jwt)


@warehouse_blueprint.route('/<warehouse_id>', methods=['PUT'])
@validate_token
def update_warehouse(warehouse_id, jwt):
    """Update a warehouse."""
    logger.debug(f"received request to update warehouse with id: {warehouse_id}")
    warehouse_data = request.get_json()
    adapter = WarehouseAdapter()
    return adapter.update_warehouse_by_id(jwt, warehouse_id, warehouse_data)


@warehouse_blueprint.route('/<warehouse_id>', methods=['DELETE'])
@validate_token
def delete_warehouse(warehouse_id, jwt):
    """Delete a warehouse."""
    logger.debug(f"received request to delete warehouse with id: {warehouse_id}")
    adapter = WarehouseAdapter()
    return adapter.delete_warehouse_by_id(jwt, warehouse_id)