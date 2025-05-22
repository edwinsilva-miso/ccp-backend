import logging

from flask import Blueprint, request

from ..adapters.warehouse_stock_item_adapter import WarehouseStockItemAdapter
from ..utils.commons import validate_token

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

warehouse_stock_item_blueprint = Blueprint('warehouse_stock_item', __name__, url_prefix='/bff/v1/web/warehouse-stock-items')


@warehouse_stock_item_blueprint.route('', methods=['POST'])
@validate_token
def create_warehouse_stock_item(jwt):
    """Create a new warehouse stock item."""
    logger.debug("received request to create a new warehouse stock item")

    warehouse_stock_item_data = request.get_json()

    adapter = WarehouseStockItemAdapter()
    return adapter.create_warehouse_stock_item(jwt, warehouse_stock_item_data)


@warehouse_stock_item_blueprint.route('/<item_id>', methods=['GET'])
@validate_token
def get_warehouse_stock_item(item_id, jwt):
    """Get a warehouse stock item by ID."""
    logger.debug(f"received request to get warehouse stock item with id: {item_id}")
    adapter = WarehouseStockItemAdapter()
    return adapter.get_warehouse_stock_item_by_id(jwt, item_id)


@warehouse_stock_item_blueprint.route('/warehouse/<warehouse_id>', methods=['GET'])
@validate_token
def get_warehouse_stock_items_by_warehouse(warehouse_id, jwt):
    """Get all warehouse stock items for a warehouse."""
    logger.debug(f"received request to get all warehouse stock items for warehouse with id: {warehouse_id}")
    adapter = WarehouseStockItemAdapter()
    return adapter.get_warehouse_stock_items_by_warehouse(jwt, warehouse_id)


@warehouse_stock_item_blueprint.route('/<item_id>', methods=['PUT'])
@validate_token
def update_warehouse_stock_item(item_id, jwt):
    """Update a warehouse stock item."""
    logger.debug(f"received request to update warehouse stock item with id: {item_id}")
    warehouse_stock_item_data = request.get_json()
    adapter = WarehouseStockItemAdapter()
    return adapter.update_warehouse_stock_item_by_id(jwt, item_id, warehouse_stock_item_data)


@warehouse_stock_item_blueprint.route('/<item_id>', methods=['DELETE'])
@validate_token
def delete_warehouse_stock_item(item_id, jwt):
    """Delete a warehouse stock item."""
    logger.debug(f"received request to delete warehouse stock item with id: {item_id}")
    adapter = WarehouseStockItemAdapter()
    return adapter.delete_warehouse_stock_item_by_id(jwt, item_id)