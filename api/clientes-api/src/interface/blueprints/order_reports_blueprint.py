import logging

from flask import Blueprint, jsonify, request

from ..decorator.token_decorator import token_required
from ...application.generate_reports import GenerateReports
from ...application.get_reports_by_user import GetReportsByUser
from ...infrastructure.adapters.order_reports_adapter import OrderReportsAdapter
from ...infrastructure.adapters.report_queries_adapter import ReportQueriesAdapter

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)
logger = logging.getLogger(__name__)

order_reports_adapter = OrderReportsAdapter()
report_queries_adapter = ReportQueriesAdapter()
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

    use_case = GenerateReports(order_reports_adapter, report_queries_adapter)
    response = use_case.execute(data)
    return jsonify(response), 200

@reports_blueprint.route('/<string:user_id>', methods=['GET'])
@token_required(['DIRECTIVO'])
def get_reports_by_user(user_id: str):
    """
    Endpoint to retrieve reports by user ID.
    """
    if not user_id:
        logger.error("User ID is required.")
        return jsonify({'msg': 'User ID is required.'}), 400

    logger.debug("Retrieving reports for user ID: %s", user_id)
    use_case = GetReportsByUser(order_reports_adapter)
    reports = use_case.execute(user_id)
    return jsonify([report.to_dict() for report in reports]), 200