import os
import logging

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify
from google.auth import default

from src.interface.blueprints.video_blueprint import video_blueprint
from src.infrastructure.database.models import db
from .application.errors.errors import ApiError
from .interface.blueprints.management_blueprint import management_blueprint

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.DEBUG)
logging.getLogger().setLevel(logging.DEBUG)  # Root logger

# Gunicorn compatibility: Make Flask debugger and handlers talk to Gunicorn's logger
gunicorn_error_logger = logging.getLogger('gunicorn.error')
logging.getLogger().handlers = gunicorn_error_logger.handlers
logging.getLogger('flask.app').handlers = gunicorn_error_logger.handlers
logging.getLogger('flask.app').setLevel(logging.DEBUG)
logging.getLogger('werkzeug').setLevel(logging.DEBUG)


def create_app():
    """
    Create and configure the Flask application.
    """
    token_info = requests.get(
        "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/email",
        headers={"Metadata-Flavor": "Google"}
    )
    logging.debug(f"Service account used by this VM/container: {token_info.text}")

    creds, project = default()
    logging.debug(f"Current GCP Project: {project}")
    logging.debug(f"Using Service Account (token): {getattr(creds, 'service_account_email', None)}")

    logging.debug('Initializing microservice application')
    app = Flask(__name__)
    logging.debug('Flask application instance created')

    DATABASE_URL = (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )

    # Configure database
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize extensions
    logging.debug('Initializing database connection')
    db.init_app(app)
    logging.debug('Database initialization completed')

    # Register blueprints
    app.register_blueprint(management_blueprint)
    app.register_blueprint(video_blueprint, url_prefix="/api/videos")

    # Error handler for API errors
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

    # Create database tables if they don't exist
    with app.app_context():
        logging.debug('Creating database tables if they do not exist')
        db.create_all()
        logging.debug('Database tables creation completed')

    return app


if __name__ == "__main__":
    app = create_app()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)