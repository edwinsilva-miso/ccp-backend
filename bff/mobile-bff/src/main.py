import logging

from dotenv import load_dotenv
from flask import Flask

loaded = load_dotenv('.env.development')

from .blueprints.management_blueprint import management_blueprint
from .blueprints.users_blueprint import users_blueprint
from .blueprints.products_blueprint import products_blueprint
from .blueprints.clients_blueprint import orders_blueprint
from .blueprints.routes_blueprint import routes_blueprint
from .blueprints.salesman_blueprint import salesman_blueprint
from .blueprints.client_visit_record_blueprint import client_visit_record_blueprint
from .blueprints.deliveries_blueprint import deliveries_blueprint
from .blueprints.videos_blueprint import videos_blueprint
from .blueprints.recommendation_blueprint import recommendation_blueprint

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
    app.register_blueprint(products_blueprint)
    app.register_blueprint(orders_blueprint)
    app.register_blueprint(routes_blueprint)
    app.register_blueprint(salesman_blueprint)
    app.register_blueprint(client_visit_record_blueprint)
    app.register_blueprint(deliveries_blueprint)
    app.register_blueprint(videos_blueprint)
    app.register_blueprint(recommendation_blueprint)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5001, debug=True)
