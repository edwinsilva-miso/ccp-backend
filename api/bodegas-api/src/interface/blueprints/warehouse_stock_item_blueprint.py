import logging

from flask import Blueprint, request, jsonify

from ..decorators.token_decorator import token_required
from ...application.warehouse_stock_item.create_warehouse_stock_item import CreateWarehouseStockItem
from ...application.warehouse_stock_item.update_warehouse_stock_item import UpdateWarehouseStockItem
from ...application.warehouse_stock_item.get_warehouse_stock_item_by_id import GetWarehouseStockItemById
from ...application.warehouse_stock_item.get_warehouse_stock_items_by_warehouse_id import GetWarehouseStockItemsByWarehouseId
from ...application.warehouse_stock_item.delete_warehouse_stock_item import DeleteWarehouseStockItem
from ...application.errors.errors import ValidationApiError, ResourceNotFoundError
from ...domain.entities.warehouse_stock_item_dto import WarehouseStockItemDTO
from ...infrastructure.adapters.warehouse_stock_item_adapter import WarehouseStockItemAdapter

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

warehouse_stock_item_adapter = WarehouseStockItemAdapter()

warehouse_stock_item_blueprint = Blueprint('warehouse_stock_item', __name__, url_prefix='/api/v1/warehouse-stock-items')


@warehouse_stock_item_blueprint.route('', methods=['POST'])
@token_required(['VENDEDOR'])
def create_warehouse_stock_item():
    """
    Endpoint to create a new warehouse stock item.
    """
    data = request.get_json()
    required_fields = ['warehouse_id', 'item_id', 'hallway', 'shelf']
    if not data or not all(key in data for key in required_fields):
        logging.error("missing required fields in request data: %s", data)
        raise ValidationApiError

    logging.debug("starting warehouse stock item creation process with data: %s", data)
    warehouse_stock_item = WarehouseStockItemDTO(
        warehouse_stock_item_id=None,
        warehouse_id=data['warehouse_id'],
        item_id=data['item_id'],
        bar_code=data.get('bar_code'),
        identification_code=data.get('identification_code'),
        width=data.get('width'),
        height=data.get('height'),
        depth=data.get('depth'),
        weight=data.get('weight'),
        hallway=data['hallway'],
        shelf=data['shelf'],
        sold=data.get('sold', False)
    )
    use_case = CreateWarehouseStockItem(warehouse_stock_item_adapter)
    response = use_case.execute(warehouse_stock_item)
    return jsonify(response.to_dict()), 201


@warehouse_stock_item_blueprint.route('/<item_id>', methods=['PUT'])
@token_required(['VENDEDOR'])
def update_warehouse_stock_item(item_id):
    """
    Endpoint to update an existing warehouse stock item.
    """
    data = request.get_json()
    required_fields = ['warehouse_id', 'item_id', 'hallway', 'shelf']
    if not data or not all(key in data for key in required_fields):
        logging.error("Missing required fields in request data.")
        raise ValidationApiError

    logging.debug("starting warehouse stock item update process for item_id: %s with data: %s", item_id, data)
    warehouse_stock_item = WarehouseStockItemDTO(
        warehouse_stock_item_id=item_id,
        warehouse_id=data['warehouse_id'],
        item_id=data['item_id'],
        bar_code=data.get('bar_code'),
        identification_code=data.get('identification_code'),
        width=data.get('width'),
        height=data.get('height'),
        depth=data.get('depth'),
        weight=data.get('weight'),
        hallway=data['hallway'],
        shelf=data['shelf'],
        sold=data.get('sold', False)
    )
    try:
        use_case = UpdateWarehouseStockItem(warehouse_stock_item_adapter)
        response = use_case.execute(warehouse_stock_item)
        return jsonify(response.to_dict()), 200
    except ResourceNotFoundError:
        raise ResourceNotFoundError


@warehouse_stock_item_blueprint.route('/<item_id>', methods=['GET'])
@token_required(['VENDEDOR'])
def get_warehouse_stock_item(item_id):
    """
    Endpoint to get a warehouse stock item by its ID.
    """
    if not item_id:
        logging.error("missing item id in request")
        raise ValidationApiError

    logging.debug("starting warehouse stock item retrieval process for item_id: %s", item_id)
    try:
        use_case = GetWarehouseStockItemById(warehouse_stock_item_adapter)
        warehouse_stock_item = use_case.execute(item_id)
        return jsonify(warehouse_stock_item.to_dict()), 200
    except ResourceNotFoundError:
        raise ResourceNotFoundError


@warehouse_stock_item_blueprint.route('/warehouse/<warehouse_id>', methods=['GET'])
@token_required(['VENDEDOR'])
def get_warehouse_stock_items_by_warehouse(warehouse_id):
    """
    Endpoint to get all warehouse stock items for a given warehouse.
    """
    if not warehouse_id:
        logging.error("missing warehouse id in request")
        raise ValidationApiError

    logging.debug("starting warehouse stock items retrieval process for warehouse_id: %s", warehouse_id)
    use_case = GetWarehouseStockItemsByWarehouseId(warehouse_stock_item_adapter)
    warehouse_stock_items = use_case.execute(warehouse_id)
    return jsonify([item.to_dict() for item in warehouse_stock_items]), 200


@warehouse_stock_item_blueprint.route('/<item_id>', methods=['DELETE'])
@token_required(['VENDEDOR'])
def delete_warehouse_stock_item(item_id):
    """
    Endpoint to delete a warehouse stock item by its ID.
    """
    if not item_id:
        logging.error("Missing item ID in request.")
        raise ValidationApiError

    logging.debug("starting warehouse stock item deletion process for item_id: %s", item_id)
    try:
        use_case = DeleteWarehouseStockItem(warehouse_stock_item_adapter)
        result = use_case.execute(item_id)
        return jsonify({"success": result}), 200
    except ResourceNotFoundError:
        raise ResourceNotFoundError
