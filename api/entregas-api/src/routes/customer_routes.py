from flask import Blueprint, request, jsonify
from src.models.models import Delivery

customer_bp = Blueprint('customer', __name__, url_prefix='/api/customer')

@customer_bp.route('/deliveries', methods=['GET'])
def get_customer_deliveries():
    """Get all deliveries for a customer."""
    customer_id = request.args.get('customer_id')
    
    if not customer_id:
        return jsonify({'error': 'customer_id parameter is required'}), 400
    
    deliveries = Delivery.query.filter_by(customer_id=customer_id).all()
    return jsonify([delivery.to_dict() for delivery in deliveries])

@customer_bp.route('/deliveries/<int:delivery_id>', methods=['GET'])
def get_delivery(delivery_id):
    """Get a specific delivery for a customer."""
    delivery = Delivery.query.get_or_404(delivery_id)
    
    # Check if the requester is the customer
    customer_id = request.args.get('customer_id')
    if not customer_id or int(customer_id) != delivery.customer_id:
        return jsonify({'error': 'Unauthorized access'}), 403
    
    return jsonify(delivery.to_dict())