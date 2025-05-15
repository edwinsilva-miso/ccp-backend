import logging
import os

from dotenv import load_dotenv
from flask import Flask, jsonify

# Load environment variables
loaded = load_dotenv('.env.development')

logging.basicConfig(level=logging.DEBUG)

from .models.models import db
from .blueprints.seller_blueprints import seller_bp
from .blueprints.customer_blueprints import customer_blueprint
from .config import config


def create_app(config_name=None):
    """
    Create and configure the Flask application.
    """
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')

    logging.debug(f'deliveries microservice started in {config_name} mode')
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)

    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

    # Register blueprints
    app.register_blueprint(seller_bp)
    app.register_blueprint(customer_blueprint)

    # Error handler for API errors
    class ApiError(Exception):
        def __init__(self, code, description):
            self.code = code
            self.description = description

    @app.errorhandler(ApiError)
    def handle_error(error):
        """
        Handle errors and return a JSON response.
        """
        logging.error(f"Error: {error.code}, {error.description}")
        response = {
            "msg": error.description
        }
        return jsonify(response), error.code

    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({"status": "healthy"}), 200

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
