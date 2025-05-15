from flask import Blueprint, request, jsonify
from ..services.seller_service import SellerService

seller_blueprint = Blueprint('seller', __name__, url_prefix='/api/seller')

@seller_blueprint.route('/deliveries', methods=['POST'])
def create_delivery():
    """Create a new delivery."""
    data = request.json

    # Validate required fields
    required_fields = ['customer_id', 'seller_id', 'description']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400

    # Use service to create delivery
    delivery = SellerService.create_delivery(data)

    return jsonify(delivery.to_dict()), 201

@seller_blueprint.route('/deliveries', methods=['GET'])
def get_seller_deliveries():
    """Get all deliveries for a seller."""
    seller_id = request.args.get('seller_id')

    if not seller_id:
        return jsonify({'error': 'seller_id parameter is required'}), 400

    # Use service to get deliveries
    deliveries = SellerService.get_seller_deliveries(seller_id)

    return jsonify([delivery.to_dict() for delivery in deliveries])

@seller_blueprint.route('/deliveries/<uuid:delivery_id>', methods=['GET'])
def get_delivery(delivery_id):
    """Get a specific delivery."""
    seller_id = request.args.get('seller_id')

    if not seller_id:
        return jsonify({'error': 'seller_id parameter is required'}), 400

    # Use service to get delivery
    delivery = SellerService.get_delivery(delivery_id, seller_id)

    if not delivery:
        return jsonify({'error': 'Delivery not found or unauthorized access'}), 404

    return jsonify(delivery.to_dict())

@seller_blueprint.route('/deliveries/order/<uuid:order_id>', methods=['GET'])
def get_delivery_by_order_id(order_id):
    """Get a specific delivery by order_id."""
    seller_id = request.args.get('seller_id')

    if not seller_id:
        return jsonify({'error': 'seller_id parameter is required'}), 400

    # Use service to get delivery by order_id
    delivery = SellerService.get_delivery_by_order_id(order_id, seller_id)

    if not delivery:
        return jsonify({'error': 'Delivery not found or unauthorized access'}), 404

    return jsonify(delivery.to_dict())

@seller_blueprint.route('/deliveries/<uuid:delivery_id>', methods=['PUT'])
def update_delivery(delivery_id):
    """Update a delivery."""
    data = request.json

    if 'seller_id' not in data:
        return jsonify({'error': 'seller_id is required'}), 400

    # Use service to update delivery
    delivery = SellerService.update_delivery(delivery_id, data)

    if not delivery:
        return jsonify({'error': 'Delivery not found or unauthorized access'}), 404

    return jsonify(delivery.to_dict())

@seller_blueprint.route('/deliveries/<uuid:delivery_id>', methods=['DELETE'])
def delete_delivery(delivery_id):
    """Delete a delivery."""
    seller_id = request.args.get('seller_id')

    if not seller_id:
        return jsonify({'error': 'seller_id parameter is required'}), 400

    # Use service to delete delivery
    success = SellerService.delete_delivery(delivery_id, seller_id)

    if not success:
        return jsonify({'error': 'Delivery not found or unauthorized access'}), 404

    return jsonify({'message': 'Delivery deleted successfully'}), 200

@seller_blueprint.route('/deliveries/<uuid:delivery_id>/status', methods=['POST'])
def add_status_update(delivery_id):
    """Add a status update to a delivery."""
    data = request.json

    if 'seller_id' not in data:
        return jsonify({'error': 'seller_id is required'}), 400

    if 'status' not in data:
        return jsonify({'error': 'Missing required field: status'}), 400

    # Use service to add status update
    status_update = SellerService.add_status_update(delivery_id, data)

    if not status_update:
        return jsonify({'error': 'Delivery not found or unauthorized access'}), 404

    return jsonify(status_update.to_dict()), 201
