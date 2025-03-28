import logging
from flask import Flask

from .interface.management_blueprint import management_blueprint

logging.basicConfig(level=logging.DEBUG)

def create_app():
    """
    Create and configure the Flask application.
    """
    logging.debug('Start application')
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(management_blueprint)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5100, debug=True)
