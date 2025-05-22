from flask import Blueprint, jsonify
from datetime import datetime
import logging

# Import db from the database module
try:
    from src.infrastructure.database import db
except ImportError:
    # Mock db for testing if not available
    db = None
    logging.warning("Database module not imported in management_blueprint")

management_blueprint = Blueprint('management', __name__)

def get_health_status():
    """
    Get the health status of the service.
    Returns a dictionary with status and timestamp.
    """
    return {
        "status": "OK",
        "timestamp": datetime.utcnow().isoformat() + 'Z'
    }

def get_database_status():
    """
    Check database connectivity and return status.
    Returns a dictionary with status and optional error message.
    """
    try:
        if db is None:
            return {"status": "Error", "message": "Database module not available"}

        # Execute a simple query to check database connectivity
        db.session.execute("SELECT 1")
        return {"status": "OK"}
    except Exception as e:
        error_message = str(e)
        logging.error(f"Database connection error: {error_message}")
        return {"status": "Error", "message": error_message}

@management_blueprint.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify if the service is running.
    """
    return jsonify({"status": "UP"}), 200

@management_blueprint.route('/health/detailed', methods=['GET'])
def detailed_health_check():
    """
    Detailed health check endpoint that includes service and database status.
    """
    health_status = get_health_status()
    db_status = get_database_status()

    response = {
        "service": health_status,
        "database": db_status
    }

    status_code = 200 if db_status["status"] == "OK" else 500
    return jsonify(response), status_code
