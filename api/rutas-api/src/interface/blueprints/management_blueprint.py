from flask import Blueprint, jsonify, current_app

management_blueprint = Blueprint('management', __name__)

@management_blueprint.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify if the service is running.
    """
    current_app.logger.info("Health check endpoint accessed")

    return jsonify({"status": "UP"}), 200
