import logging
import threading

from dotenv import load_dotenv
from flask import Flask, jsonify

loaded = load_dotenv('.env.development')

from .interface.blueprints.management_blueprint import management_blueprint
from .interface.blueprints.products_blueprint import products_blueprint
from .interface.consumer.update_products_stock_consumer import UpdateProductsStockConsumer
from .interface.blueprints.products_manufacturer_blueprint import products_manufacturer_blueprint
from .application.errors.errors import ApiError
from .infrastructure.database.declarative_base import Base, engine

logging.basicConfig(level=logging.DEBUG)


def initialize_rabbitmq_consumers():
    """Initialize all RabbitMQ consumers"""
    # Create and start the stock update consumer
    stock_consumer = UpdateProductsStockConsumer()
    stock_consumer.start_consuming()


def create_app():
    """
    Create and configure the Flask application.
    """
    logging.debug('products microservice started')
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(management_blueprint)
    app.register_blueprint(products_blueprint)
    app.register_blueprint(products_manufacturer_blueprint)

    # Initialize the consumer
    logging.debug(">> Initialize the consumer")
    # Start consumers in a separate thread to not block the main application
    consumer_thread = threading.Thread(
        target=initialize_rabbitmq_consumers,
        daemon=True
    )
    consumer_thread.start()

    # Create schema
    logging.debug(">> Create schema")
    Base.metadata.create_all(engine)

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
    app.run(host='0.0.0.0', port=5103, debug=True)
