import functools
import logging

from flask import Blueprint, jsonify, request

from ..adapters.products_adapter import ProductsAdapter
from ..utils.commons import token_required

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

products_blueprint = Blueprint('products', __name__, url_prefix='/bff/v1/mobile/products')


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
