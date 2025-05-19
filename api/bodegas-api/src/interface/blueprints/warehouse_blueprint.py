import logging

from flask import Blueprint, request, jsonify

from ..decorators.token_decorator import token_required
from ...application.warehouse.create_warehouse import CreateWarehouse
from ...application.warehouse.update_warehouse import UpdateWarehouse
from ...application.warehouse.get_warehouse_by_id import GetWarehouseById
from ...application.warehouse.get_all_warehouses import GetAllWarehouses
from ...application.warehouse.get_warehouses_by_administrator_id import GetWarehousesByAdministratorId
from ...application.warehouse.delete_warehouse import DeleteWarehouse
from ...application.errors.errors import ValidationApiError, ResourceNotFoundError
from ...domain.entities.warehouse_dto import WarehouseDTO
from ...infrastructure.adapters.warehouse_adapter import WarehouseAdapter

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

warehouse_adapter = WarehouseAdapter()

warehouse_blueprint = Blueprint('warehouse', __name__, url_prefix='/api/v1/warehouses')


@warehouse_blueprint.route('', methods=['POST'])
@token_required(['VENDEDOR', 'DIRECTIVO'])
def create_warehouse():
    """
    Endpoint to create a new warehouse.
    """
    data = request.get_json()
    if not data or not all(key in data for key in ['location', 'description', 'name', 'administrator_id']):
        logging.error("missing required fields in request data: %s", data)
        raise ValidationApiError

    logging.debug("starting warehouse creation process with data: %s", data)
    warehouse = WarehouseDTO(
        warehouse_id=None,
        location=data['location'],
        description=data['description'],
        name=data['name'],
        administrator_id=data['administrator_id']
    )
    use_case = CreateWarehouse(warehouse_adapter)
    response = use_case.execute(warehouse)
    return jsonify(response.to_dict()), 201


@warehouse_blueprint.route('/<warehouse_id>', methods=['PUT'])
@token_required(['VENDEDOR', 'DIRECTIVO'])
def update_warehouse(warehouse_id):
    """
    Endpoint to update an existing warehouse.
    """
    data = request.get_json()
    if not data or not all(key in data for key in ['location', 'description', 'name', 'administrator_id']):
        logging.error("Missing required fields in request data.")
        raise ValidationApiError

    logging.debug("starting warehouse update process for warehouse_id: %s with data: %s", warehouse_id, data)
    warehouse = WarehouseDTO(
        warehouse_id=warehouse_id,
        location=data['location'],
        description=data['description'],
        name=data['name'],
        administrator_id=data['administrator_id']
    )
    try:
        use_case = UpdateWarehouse(warehouse_adapter)
        response = use_case.execute(warehouse)
        return jsonify(response.to_dict()), 200
    except ResourceNotFoundError:
        raise ResourceNotFoundError


@warehouse_blueprint.route('/<warehouse_id>', methods=['GET'])
@token_required(['VENDEDOR', 'DIRECTIVO'])
def get_warehouse(warehouse_id):
    """
    Endpoint to get a warehouse by its ID.
    """
    if not warehouse_id:
        logging.error("missing warehouse id in request")
        raise ValidationApiError

    logging.debug("starting warehouse retrieval process for warehouse_id: %s", warehouse_id)
    try:
        use_case = GetWarehouseById(warehouse_adapter)
        warehouse = use_case.execute(warehouse_id)
        return jsonify(warehouse.to_dict()), 200
    except ResourceNotFoundError:
        raise ResourceNotFoundError


@warehouse_blueprint.route('', methods=['GET'])
@token_required(['VENDEDOR', 'DIRECTIVO'])
def get_all_warehouses():
    """
    Endpoint to get all warehouses.
    """
    administrator_id = request.args.get('administrator_id')

    if administrator_id:
        logging.debug(f"starting warehouses retrieval process for administrator_id: {administrator_id}")
        use_case = GetWarehousesByAdministratorId(warehouse_adapter)
        warehouses = use_case.execute(administrator_id)
    else:
        logging.debug("starting all warehouses retrieval process")
        use_case = GetAllWarehouses(warehouse_adapter)
        warehouses = use_case.execute()

    return jsonify([warehouse.to_dict() for warehouse in warehouses]), 200


@warehouse_blueprint.route('/<warehouse_id>', methods=['DELETE'])
@token_required(['VENDEDOR', 'DIRECTIVO'])
def delete_warehouse(warehouse_id):
    """
    Endpoint to delete a warehouse by its ID.
    """
    if not warehouse_id:
        logging.error("Missing warehouse ID in request.")
        raise ValidationApiError

    logging.debug("starting warehouse deletion process for warehouse_id: %s", warehouse_id)
    try:
        use_case = DeleteWarehouse(warehouse_adapter)
        result = use_case.execute(warehouse_id)
        return jsonify({"success": result}), 200
    except ResourceNotFoundError:
        raise ResourceNotFoundError
