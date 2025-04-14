import logging

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

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

    CORS(app, resources={
        r"/bff/*": {
            "origins": [
                "http://localhost:4200",
                "https://proyecto-final-644666181364.uc.r.appspot.com",
                "https://proyecto-final-644666181364.us-central1.run.app"
            ]
        }
    }, supports_credentials=True)

    # Register blueprints
    app.register_blueprint(management_blueprint)
    app.register_blueprint(users_blueprint)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
