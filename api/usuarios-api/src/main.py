import logging

from dotenv import load_dotenv
from flask import Flask, jsonify

loaded = load_dotenv('.env.development')

from .interface.blueprints.management_blueprint import management_blueprint
from .interface.blueprints.users_blueprint import user_blueprint
from .application.errors.errors import ApiError
from .infrastructure.database.declarative_base import Base, engine

logging.basicConfig(level=logging.DEBUG)


def create_app():
    """
    Create and configure the Flask application.
    """
    logging.debug('users microservice started')
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(management_blueprint)
    app.register_blueprint(user_blueprint)

    # Create schema
    logging.debug(">> Create schema")
    Base.metadata.create_all(engine)

    # Error handling
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

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
