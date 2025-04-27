import os
import logging
import sys

from flask import Flask, jsonify
from dotenv import load_dotenv
# from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

loaded = load_dotenv('.env.development')

from .api.v1.routes import routes_blueprint
from .api.v1.optimizations import optimizations_blueprint
from .infrastructure.config import Config
from .infrastructure.external.openroute_service_client import OpenRouteServiceClient
from .infrastructure.repositories.sqlalchemy_route_repository import Base, SQLAlchemyRouteRepository
from .domain.services.optimization_service import OptimizationService
from .api.error_handlers import register_error_handlers


# Configure the logging handler to output to stdout (Kubernetes reads from stdout/stderr)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)  # Allow DEBUG messages in the output handler
formatter = logging.Formatter(
    fmt='[%(asctime)s] [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
handler.setFormatter(formatter)

# Get the root logger and configure it
logging.basicConfig(level=logging.DEBUG, handlers=[handler])

# Optional: Configure specific logger (SQLAlchemyRouteRepository in this case)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Register CORS | discuss with team
    #    CORS(app)

    # Setup database
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    session_factory = sessionmaker(bind=engine)
    session = scoped_session(session_factory)

    # Create tables if they don't exist
    Base.metadata.create_all(engine)

    # Initialize repositories
    route_repository = SQLAlchemyRouteRepository(session=session)

    # Initialize services
    openroute_client = OpenRouteServiceClient(
        api_key=app.config['OPENROUTE_API_KEY'],
        base_url=app.config['OPENROUTE_BASE_URL']
    )
    optimization_service = OptimizationService(openroute_client=openroute_client)

    # Add services to app context
    app.route_repository = route_repository
    app.openroute_client = openroute_client
    app.optimization_service = optimization_service

    # Register blueprints
    app.register_blueprint(routes_blueprint, url_prefix='/api/v1')
    app.register_blueprint(optimizations_blueprint, url_prefix='/api/v1')

    # Register error handlers
    register_error_handlers(app)

    # Root endpoint
    @app.route('/')
    def root():
        return jsonify({"message": "Welcome to Rutas API"})

    # Health check endpoint
    @app.route('/health')
    def health():
        return jsonify({"status": "healthy"})

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
