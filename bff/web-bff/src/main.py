import logging

from dotenv import load_dotenv
from flask import Flask

loaded = load_dotenv('.env.development')

from .blueprints.management_blueprint import management_blueprint
from .blueprints.users_blueprint import users_blueprint

logging.basicConfig(level=logging.DEBUG)


def create_app():
    """
    Create and configure the Flask application.
    """
    logging.debug('BFF users microservice started')
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(management_blueprint)
    app.register_blueprint(users_blueprint)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
