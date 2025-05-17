from flask import Blueprint, jsonify

management_blueprint = Blueprint('management', __name__)


@management_blueprint.route('/health', methods=['GET'])
def health_check():
    """
    Endpoint to check the health of the service.
    """
    return jsonify({"status": "healthy"}), 200