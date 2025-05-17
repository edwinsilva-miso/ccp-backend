import logging

from flask import Blueprint, jsonify, request

from ..decorator.token_decorator import token_required
from ...application.create_product import CreateProduct
from ...application.delete_product import DeleteProduct
from ...application.errors.errors import ValidationApiError
from ...application.get_all_products import GetAllProducts
from ...application.get_product_by_id import GetProductById
from ...application.update_product import UpdateProduct
from ...domain.entities.product_dto import ProductDTO
from ...infrastructure.adapters.product_adapter import ProductAdapter


products_blueprint = Blueprint('products', __name__, url_prefix='/api/v1/products')

products_adapter = ProductAdapter()


@products_blueprint.route('/', methods=['POST'])
@token_required(['DIRECTIVO'])
def create_product():
    data = request.get_json()
    if not data or not all(key in data for key in (
            'name', 'brand', 'description', 'manufacturerId', 'details', 'stock', 'storageConditions', 'price', 'currency', 'deliveryTime',
            'images')):
        logging.error("Missing required fields in request data.")
        raise ValidationApiError

    product = ProductDTO(
        id=None,
        name=data['name'],
        brand=data['brand'],
        manufacturer_id=data['manufacturerId'],
        description=data['description'],
        stock=data['stock'],
        details=data['details'],
        storage_conditions=data['storageConditions'],
        price=data['price'],
        currency=data['currency'],
        delivery_time=data['deliveryTime'],
        images=data['images'],
        created_at=None,
        updated_at=None
    )
    use_case = CreateProduct(products_adapter)
    product_id = use_case.execute(product)
    return jsonify({'id': product_id}), 201


@products_blueprint.route('/', methods=['GET'])
@token_required(['DIRECTIVO', 'CLIENTE', 'VENDEDOR'])
def get_all_products():
    use_case = GetAllProducts(products_adapter)
    products = use_case.execute()
    return jsonify([product.to_dict() for product in products]), 200


@products_blueprint.route('/<string:product_id>', methods=['GET'])
@token_required(['DIRECTIVO', 'CLIENTE', 'VENDEDOR'])
def get_product_by_id(product_id):
    use_case = GetProductById(products_adapter)
    product = use_case.execute(product_id)
    return jsonify(product.to_dict()), 200


@products_blueprint.route('/<string:product_id>', methods=['PUT'])
@token_required(['DIRECTIVO'])
def update_product(product_id):
    data = request.get_json()
    if not data or not all(key in data for key in (
            'name', 'brand', 'description', 'manufacturerId', 'stock', 'details', 'storageConditions', 'price', 'currency', 'deliveryTime',
            'images')):
        logging.error("Missing required fields in request data.")
        raise ValidationApiError

    product = ProductDTO(
        id=None,
        name=data['name'],
        brand=data['brand'],
        manufacturer_id=data['manufacturerId'],
        description=data['description'],
        stock=data['stock'],
        details=data['details'],
        storage_conditions=data['storageConditions'],
        price=data['price'],
        currency=data['currency'],
        delivery_time=data['deliveryTime'],
        images=data['images'],
        created_at=None,
        updated_at=None
    )
    use_case = UpdateProduct(products_adapter)
    response = use_case.execute(product_id, product)
    return jsonify(response.to_dict()), 200


@products_blueprint.route('/<string:product_id>', methods=['DELETE'])
@token_required(['DIRECTIVO'])
def delete_product(product_id):
    use_case = DeleteProduct(products_adapter)
    use_case.execute(product_id)
    return {}, 204
