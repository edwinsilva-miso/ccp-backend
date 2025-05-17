import logging
import functools

from flask import Blueprint, request, jsonify

from ..adapters.reports_adapter import ReportsAdapter

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

reports_blueprint = Blueprint('reports', __name__, url_prefix='/bff/v1/web/reports')

def token_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            logger.error("Missing Authorization header.")
            return jsonify({'msg': 'Unauthorized'}), 401

        jwt = token.split('Bearer ')[-1] if 'Bearer ' in token else token
        kwargs['jwt'] = jwt
        return f(*args, **kwargs)

    return decorated_function

@reports_blueprint.route('/<user_id>', methods=['GET'])
@token_required
def get_report_by_user_id(user_id, jwt):
    """
    Get a report by user ID.
    :param user_id: ID of the user to retrieve the report for.
    :param jwt: JWT token for authorization.
    :return: The report data
    """
    logger.debug(f"Received request to get report by user ID: {user_id}")
    logger.debug("Retrieving report by user ID from BFF Web.")
    adapter = ReportsAdapter()
    return adapter.get_report_by_user_id(jwt, user_id)

@reports_blueprint.route('/generate', methods=['POST'])
@token_required
def generate_report(jwt):
    """
    Generate a report.
    :param jwt: JWT token for authorization.
    :return: The report data
    """
    logger.debug("Received request to generate report.")
    logger.debug("Generating report from BFF Web.")
    data = request.get_json()
    adapter = ReportsAdapter()
    return adapter.generate_report(jwt, data)