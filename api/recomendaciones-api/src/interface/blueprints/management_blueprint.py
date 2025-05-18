from flask import Blueprint, jsonify

management_blueprint = Blueprint('management', __name__)

@management_blueprint.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify if the service is running.
    """
    return jsonify({"status": "UP"}), 200