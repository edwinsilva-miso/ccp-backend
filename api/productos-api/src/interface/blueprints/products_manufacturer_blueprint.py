import logging

from flask import Blueprint, jsonify

from ..decorator.token_decorator import token_required
from ...application.get_product_by_manufacturer import GetProductByManufacturer
from ...infrastructure.adapters.product_adapter import ProductAdapter

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)
logger = logging.getLogger(__name__)

products_manufacturer_blueprint = Blueprint('products_manufacturers', __name__, url_prefix='/api/v1/manufacturers')

products_adapter = ProductAdapter()


@products_manufacturer_blueprint.route('/<string:manufacturer_id>/products', methods=['GET'])
@token_required(['DIRECTIVO', 'CLIENTE', 'VENDEDOR'])
def get_products_manufacturer(manufacturer_id):
    use_case = GetProductByManufacturer(products_adapter)
    products = use_case.execute(manufacturer_id)
    return jsonify([product.__dict__ for product in products]), 200
