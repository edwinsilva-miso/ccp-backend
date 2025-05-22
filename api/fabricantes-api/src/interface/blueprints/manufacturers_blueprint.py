import logging
from flask import Blueprint, jsonify, request

from ..decorators.token_decorator import token_required
from ...application.errors.errors import ValidationApiError
from ...application.create_manufacturer import CreateManufacturer
from ...application.update_manufacturer import UpdateManufacturer
from ...application.get_all_manufacturers import GetAllManufacturers
from ...application.get_manufacturer_by_id import GetManufacturerById
from ...application.get_manufacturer_by_nit import GetManufacturerByNit
from ...application.delete_manufacturer import DeleteManufacturer
from ...application.bulk_create_manufacturers import BulkCreateManufacturers
from ...domain.entities.manufacturer_dto import ManufacturerDTO
from ...infrastructure.adapters.manufacturer_adapter import ManufacturerAdapter

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)
logger = logging.getLogger(__name__)

manufacturers_blueprint = Blueprint('manufacturer', __name__, url_prefix='/api/v1/manufacturers')

manufacturers_adapter = ManufacturerAdapter()

@manufacturers_blueprint.route('/', methods=['POST'])
@token_required
def create_manufacturer():
    data = request.get_json()
    if not data or not all(key in data for key in ('name', 'phone', 'email', 'nit', 'legal_representative', 'country')):
        logging.error("Missing required fields in request data.")
        raise ValidationApiError

    manufacturer = ManufacturerDTO(
        id=None,
        nit=data['nit'],
        name=data['name'],
        address=data['address'],
        phone=data['phone'],
        email=data['email'],
        legal_representative=data['legal_representative'],
        country=data['country'],
        status=None,
        created=None,
        updated=None
    )
    use_case = CreateManufacturer(manufacturers_adapter)
    manufacturer_id = use_case.execute(manufacturer)
    return jsonify({'id': manufacturer_id}), 201

@manufacturers_blueprint.route('/', methods=['GET'])
@token_required
def get_all_manufacturer():
    use_case = GetAllManufacturers(manufacturers_adapter)
    manufacturers = use_case.execute()
    return jsonify([manufacturer.__dict__ for manufacturer in manufacturers]), 200


@manufacturers_blueprint.route('/<string:manufacturer_id>', methods=['GET'])
@token_required
def get_manufacturer_by_id(manufacturer_id):
    use_case = GetManufacturerById(manufacturers_adapter)
    manufacturer = use_case.execute(manufacturer_id)
    return jsonify(manufacturer.__dict__), 200


@manufacturers_blueprint.route('/search', methods=['GET'])
@token_required
def get_manufacturer_by_nit():
    nit = request.args.get('nit')
    if not nit:
        logging.error("Missing 'nit' query parameter.")
        raise ValidationApiError

    use_case = GetManufacturerByNit(manufacturers_adapter)
    manufacturer = use_case.execute(nit)
    return jsonify(manufacturer.__dict__), 200

@manufacturers_blueprint.route('/<string:manufacturer_id>', methods=['PUT'])
@token_required
def update_manufacturer(manufacturer_id):
    data = request.get_json()
    if not data or not all(key in data for key in ('name', 'address', 'phone', 'email', 'legal_representative', 'country', 'status')):
        logging.error("Missing required fields in request data.")
        raise ValidationApiError

    manufacturer = ManufacturerDTO(
        id=None,
        nit=None,
        name=data['name'],
        address=data['address'],
        phone=data['phone'],
        email=data['email'],
        legal_representative=data['legal_representative'],
        country=data['country'],
        status=data['status'],
        created=None,
        updated=None
    )
    use_case = UpdateManufacturer(manufacturers_adapter)
    updated = use_case.execute(manufacturer_id, manufacturer)
    return jsonify(updated.__dict__), 200

@manufacturers_blueprint.route('/<string:manufacturer_id>', methods=['DELETE'])
@token_required
def delete_manufacturer(manufacturer_id):
    use_case = DeleteManufacturer(manufacturers_adapter)
    use_case.execute(manufacturer_id)
    return {}, 204

@manufacturers_blueprint.route('/bulk-upload', methods=['POST'])
@token_required
def bulk_upload_manufacturers():
    """
    Endpoint for bulk uploading manufacturers from Excel file.
    Expects a base64 encoded Excel file in the request body under the key 'file'.
    """
    data = request.get_json()
    if not data or 'file' not in data:
        logging.error("Missing 'file' field in request data.")
        raise ValidationApiError

    try:
        excel_base64 = data['file']
        use_case = BulkCreateManufacturers(manufacturers_adapter)
        result = use_case.execute(excel_base64)

        return jsonify({
            'message': 'Proceso de carga masiva completado',
            'successful_count': result['successful_count'],
            'failed_count': result['failed_count'],
            'errors': result['errors']
        }), 200

    except Exception as e:
        logging.error(f"Error during bulk upload: {str(e)}")
        return jsonify({
            'error': 'Error procesando el archivo Excel',
            'details': str(e)
        }), 400

