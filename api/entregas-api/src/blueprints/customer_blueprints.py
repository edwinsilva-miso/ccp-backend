from flask import Blueprint, request, jsonify
from uuid import UUID
from ..services.customer_service import CustomerService

customer_blueprint = Blueprint('customer', __name__, url_prefix='/api/deliveries')

@customer_blueprint.route('/customers/<uuid:customer_id>', methods=['GET'])
def get_customer_deliveries(customer_id):
    if not customer_id:
        return jsonify({'error': 'customer_id parameter is required'}), 400

    # Use service to get deliveries
    deliveries = CustomerService.get_customer_deliveries(customer_id)

    return jsonify([delivery.to_dict() for delivery in deliveries])

@customer_blueprint.route('/<uuid:delivery_id>', methods=['GET'])
def get_delivery(delivery_id):
    """Get a specific delivery for a customer."""
    customer_id = request.args.get('customer_id')

    if not customer_id:
        return jsonify({'error': 'customer_id parameter is required'}), 400

    # Use service to get delivery
    delivery = CustomerService.get_delivery(delivery_id, customer_id)

    if not delivery:
        return jsonify({'error': 'Delivery not found or unauthorized access'}), 404

    return jsonify(delivery.to_dict())

@customer_blueprint.route('/order/<uuid:order_id>', methods=['GET'])
def get_delivery_by_order_id(order_id):
    """Get a specific delivery for a customer by order_id."""
    customer_id = request.args.get('customer_id')

    if not customer_id:
        return jsonify({'error': 'customer_id parameter is required'}), 400

    try:
        customer_id = UUID(customer_id)
    except ValueError:
        return jsonify({'error': 'Invalid customer_id format'}), 500

    # Use service to get delivery by order_id
    delivery = CustomerService.get_delivery_by_order_id(order_id, customer_id)

    if not delivery:
        return jsonify({'error': 'Delivery not found or unauthorized access'}), 404

    return jsonify(delivery.to_dict())
