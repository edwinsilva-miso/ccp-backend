import logging

from flask import Blueprint, jsonify, request

from ..decorator.token_decorator import token_required
from ...application.generate_reports import GenerateReports
from ...infrastructure.adapters.order_reports_adapter import OrderReportsAdapter

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)
logger = logging.getLogger(__name__)

order_reports_adapter = OrderReportsAdapter()
reports_blueprint = Blueprint('reports', __name__, url_prefix='/api/v1/reports')

@reports_blueprint.route('/generate', methods=['POST'])
@token_required(['DIRECTIVO'])
def generate_report():
    """
    Endpoint to generate a report.
    """
    logger.debug("Starting report generation process...")
    data = request.get_json()
    if not data:
        logger.error("No data provided in request.")
        return jsonify({'msg': 'Data is required.'}), 400

    use_case = GenerateReports(order_reports_adapter)
    response = use_case.execute(data)
    return jsonify(response), 200