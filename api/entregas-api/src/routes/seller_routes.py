from flask import Blueprint, request, jsonify
from src.models.models import db, Delivery, StatusUpdate

seller_bp = Blueprint('seller', __name__, url_prefix='/api/seller')

@seller_bp.route('/deliveries', methods=['POST'])
def create_delivery():
    """Create a new delivery."""
    data = request.json
    
    # Validate required fields
    required_fields = ['customer_id', 'seller_id', 'description']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Create new delivery
    delivery = Delivery(
        customer_id=data['customer_id'],
        seller_id=data['seller_id'],
        description=data['description'],
        estimated_delivery_date=data.get('estimated_delivery_date')
    )
    
    # Add to database
    db.session.add(delivery)
    db.session.commit()
    
    # Create initial status update if provided
    if 'initial_status' in data:
        status_update = StatusUpdate(
            delivery_id=delivery.id,
            status=data['initial_status'],
            description=data.get('status_description', 'Delivery created')
        )
        db.session.add(status_update)
        db.session.commit()
    
    return jsonify(delivery.to_dict()), 201

@seller_bp.route('/deliveries', methods=['GET'])
def get_seller_deliveries():
    """Get all deliveries for a seller."""
    seller_id = request.args.get('seller_id')
    
    if not seller_id:
        return jsonify({'error': 'seller_id parameter is required'}), 400
    
    deliveries = Delivery.query.filter_by(seller_id=seller_id).all()
    return jsonify([delivery.to_dict() for delivery in deliveries])

@seller_bp.route('/deliveries/<int:delivery_id>', methods=['GET'])
def get_delivery(delivery_id):
    """Get a specific delivery."""
    delivery = Delivery.query.get_or_404(delivery_id)
    
    # Check if the requester is the seller
    seller_id = request.args.get('seller_id')
    if not seller_id or int(seller_id) != delivery.seller_id:
        return jsonify({'error': 'Unauthorized access'}), 403
    
    return jsonify(delivery.to_dict())

@seller_bp.route('/deliveries/<int:delivery_id>', methods=['PUT'])
def update_delivery(delivery_id):
    """Update a delivery."""
    delivery = Delivery.query.get_or_404(delivery_id)
    
    # Check if the requester is the seller
    data = request.json
    if 'seller_id' not in data or data['seller_id'] != delivery.seller_id:
        return jsonify({'error': 'Unauthorized access'}), 403
    
    # Update fields
    if 'description' in data:
        delivery.description = data['description']
    if 'estimated_delivery_date' in data:
        delivery.estimated_delivery_date = data['estimated_delivery_date']
    
    db.session.commit()
    return jsonify(delivery.to_dict())

@seller_bp.route('/deliveries/<int:delivery_id>', methods=['DELETE'])
def delete_delivery(delivery_id):
    """Delete a delivery."""
    delivery = Delivery.query.get_or_404(delivery_id)
    
    # Check if the requester is the seller
    seller_id = request.args.get('seller_id')
    if not seller_id or int(seller_id) != delivery.seller_id:
        return jsonify({'error': 'Unauthorized access'}), 403
    
    db.session.delete(delivery)
    db.session.commit()
    return jsonify({'message': 'Delivery deleted successfully'}), 200

@seller_bp.route('/deliveries/<int:delivery_id>/status', methods=['POST'])
def add_status_update(delivery_id):
    """Add a status update to a delivery."""
    delivery = Delivery.query.get_or_404(delivery_id)
    
    # Check if the requester is the seller
    data = request.json
    if 'seller_id' not in data or data['seller_id'] != delivery.seller_id:
        return jsonify({'error': 'Unauthorized access'}), 403
    
    # Validate required fields
    if 'status' not in data:
        return jsonify({'error': 'Missing required field: status'}), 400
    
    # Create status update
    status_update = StatusUpdate(
        delivery_id=delivery_id,
        status=data['status'],
        description=data.get('description')
    )
    
    db.session.add(status_update)
    db.session.commit()
    
    return jsonify(status_update.to_dict()), 201