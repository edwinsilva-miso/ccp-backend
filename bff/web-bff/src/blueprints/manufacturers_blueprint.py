import functools
import logging

from flask import Blueprint, jsonify, request

from ..adapters.manufacturers_adapter import ManufacturersAdapter
from ..adapters.products_adapter import ProductsAdapter

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

manufacturers_blueprint = Blueprint('manufacturers', __name__, url_prefix='/bff/v1/web/manufacturers')


def token_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            logging.error("Missing Authorization header.")
            return jsonify({'msg': 'Unauthorized'}), 401

        jwt = token.split('Bearer ')[-1] if 'Bearer ' in token else token
        kwargs['jwt'] = jwt
        return f(*args, **kwargs)

    return decorated_function


@manufacturers_blueprint.route('/', methods=['GET'])
@token_required
def get_all_manufacturers(jwt):
    logging.debug("Received request to get all manufacturers.")
    logging.debug("Retrieving all manufacturers from BFF Web.")
    adapter = ManufacturersAdapter()
    return adapter.get_all_manufacturers(jwt)


@manufacturers_blueprint.route('/<manufacturer_id>', methods=['GET'])
@token_required
def get_manufacturer_by_id(manufacturer_id, jwt):
    logging.debug(f"Received request to get manufacturer with ID: {manufacturer_id}")
    logging.debug("Retrieving manufacturer by ID from BFF Web.")
    adapter = ManufacturersAdapter()
    return adapter.get_manufacturer_by_id(jwt, manufacturer_id)


@manufacturers_blueprint.route('/search', methods=['GET'])
@token_required
def get_manufacturer_by_nit(jwt):
    nit = request.args.get('nit')
    if not nit:
        logging.error("Missing NIT parameter.")
        return jsonify({'msg': 'NIT parameter is required.'}), 400

    logging.debug(f"Received request to get manufacturer with NIT: {nit}")
    logging.debug("Retrieving manufacturer by NIT from BFF Web.")
    adapter = ManufacturersAdapter()
    return adapter.get_manufacturer_by_nit(jwt, nit)


@manufacturers_blueprint.route('/', methods=['POST'])
@token_required
def create_manufacturer(jwt):
    logging.debug("Received request to create manufacturer.")
    manufacturer_data = request.get_json()
    if not manufacturer_data or not all(key in manufacturer_data for key in ('name', 'nit', 'address', 'phone')):
        logging.error("Missing required fields in request manufacturer_data.")
        return jsonify({'msg': 'Faltan campos requeridos.'}), 400

    logging.debug("Creating new manufacturer from BFF Web.")
    adapter = ManufacturersAdapter()
    return adapter.create_manufacturer(jwt, manufacturer_data)


@manufacturers_blueprint.route('/<manufacturer_id>', methods=['PUT'])
@token_required
def update_manufacturer(manufacturer_id, jwt):
    logging.debug(f"Received request to update manufacturer with ID: {manufacturer_id}")
    manufacturer_data = request.get_json()
    if not manufacturer_data:
        logging.error("Missing data in request manufacturer_data.")
        return jsonify({'msg': 'Datos requeridos.'}), 400

    logging.debug("Updating manufacturer from BFF Web.")
    adapter = ManufacturersAdapter()
    return adapter.update_manufacturer(jwt, manufacturer_id, manufacturer_data)


@manufacturers_blueprint.route('/<manufacturer_id>', methods=['DELETE'])
@token_required
def delete_manufacturer(manufacturer_id, jwt):
    logging.debug(f"Received request to delete manufacturer with ID: {manufacturer_id}")
    logging.debug("Deleting manufacturer from BFF Web.")
    adapter = ManufacturersAdapter()
    return adapter.delete_manufacturer(jwt, manufacturer_id)


@manufacturers_blueprint.route('/<manufacturer_id>/products', methods=['GET'])
@token_required
def get_products_by_manufacturer(manufacturer_id, jwt):
    logging.debug(f"Received request to get products by manufacturer ID: {manufacturer_id}")
    logging.debug("Retrieving products by manufacturer ID from BFF Web.")
    adapter = ProductsAdapter()
    return adapter.get_products_by_manufacturer(jwt, manufacturer_id)
