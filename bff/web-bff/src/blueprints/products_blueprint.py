import functools
import logging

from flask import Blueprint, jsonify, request

from ..adapters.products_adapter import ProductsAdapter
from ..adapters.products_bulk_adapter import ProductsBulkAdapter

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

products_blueprint = Blueprint('products', __name__, url_prefix='/bff/v1/web/products')


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


@products_blueprint.route('/', methods=['GET'])
@token_required
def get_all_products(jwt):
    logging.debug("Received request to get all products.")
    logging.debug("Retrieving all products from BFF Web.")
    adapter = ProductsAdapter()
    return adapter.get_all_products(jwt)


@products_blueprint.route('/<product_id>', methods=['GET'])
@token_required
def get_product_by_id(product_id, jwt):
    logging.debug(f"Received request to get product with ID: {product_id}")
    logging.debug("Retrieving product by ID from BFF Web.")
    adapter = ProductsAdapter()
    return adapter.get_product_by_id(jwt, product_id)


@products_blueprint.route('/', methods=['POST'])
@token_required
def create_product(jwt):
    logging.debug("Received request to create a new product.")
    data = request.get_json()
    if not data or not all(key in data for key in (
            'name', 'brand', 'description', 'manufacturerId', 'stock', 'details', 'storageConditions', 'price', 'currency',
            'deliveryTime',
            'images')):
        logging.error("Missing required fields in request data.")
        return jsonify({'msg': 'Missing required fields.'}), 400
    logging.debug("Creating a new product in BFF Web.")
    adapter = ProductsAdapter()
    return adapter.create_product(jwt, data)


@products_blueprint.route('/<product_id>', methods=['PUT'])
@token_required
def update_product(product_id, jwt):
    logging.debug("Received request to update a new product.")
    data = request.get_json()
    if not data or not all(key in data for key in (
            'name', 'brand', 'description', 'manufacturerId', 'stock', 'details', 'storageConditions', 'price', 'currency',
            'deliveryTime',
            'images')):
        logging.error("Missing required fields in request data.")
        return jsonify({'msg': 'Missing required fields.'}), 400
    logging.debug("Updating a new product in BFF Web.")
    adapter = ProductsAdapter()
    return adapter.update_product(jwt, product_id, data)


@products_blueprint.route('/<product_id>', methods=['DELETE'])
@token_required
def delete_product(product_id, jwt):
    logging.debug(f"Received request to delete product with ID: {product_id}")
    logging.debug("Deleting product by ID from BFF Web.")
    adapter = ProductsAdapter()
    return adapter.delete_product(jwt, product_id)

@products_blueprint.route('/bulk', methods=['POST'])
@token_required
def bulk_products(jwt):
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    if file and file.filename.endswith('.csv'):
        logging.debug("Received request to process bulk products.")
        logging.debug("Processing bulk products in BFF Web.")
        adapter = ProductsBulkAdapter()
        return adapter.process_file(file)
    else:
        return jsonify({"message": "Invalid file format"}), 400

