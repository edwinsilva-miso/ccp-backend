import functools
import logging

from flask import Blueprint, jsonify, request

from ..adapters.client_visit_records_adapter import ClientVisitRecordsAdapter

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)
logger = logging.getLogger(__name__)

client_visit_record_blueprint = Blueprint('client_visit_record', __name__, url_prefix='/bff/v1/mobile/salesman')

def token_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            logging.error("Missing Authorization header.")
            return jsonify({'msg': 'Unauthorized'}), 401

        jwt = token.split('Bearer ')[-1] if 'Bearer ' in token else token
        kwargs['jwt'] = jwt
        return f(*args, **kwargs)

    return decorated_function

@client_visit_record_blueprint.route('<salesman_id>/visits', methods=['GET'])
@token_required
def get_client_visit_records(jwt, salesman_id):
    """
    Get all client visit records by salesman.
    :param jwt: JWT token for authorization.
    :param salesman_id: ID of the salesman to retrieve visit records for.
    :return: The visit records data
    """
    logging.debug("Received request to get client visit records by salesman.")
    logging.debug("Retrieving all salesman's visit records from BFF Mobile")
    adapter = ClientVisitRecordsAdapter()
    return adapter.get_client_visit_records(jwt, salesman_id)

@client_visit_record_blueprint.route('<salesman_id>/visits/<record_id>', methods=['GET'])
@token_required
def get_client_visit_record(jwt, salesman_id, record_id):
    """
    Get a specific client visit record by salesman.
    :param jwt: JWT token for authorization.
    :param salesman_id: ID of the salesman to retrieve visit record for.
    :param record_id: ID of the visit record to retrieve.
    :return: The visit record data
    """
    logging.debug("Received request to get client visit record by salesman.")
    logging.debug(f"Retrieving salesman's visit record {record_id} from BFF Mobile")
    adapter = ClientVisitRecordsAdapter()
    return adapter.get_client_visit_record(jwt, salesman_id, record_id)

@client_visit_record_blueprint.route('<salesman_id>/visits', methods=['POST'])
@token_required
def add_client_visit_record(jwt, salesman_id):
    """
    Add a new client visit record by salesman.
    :param jwt: JWT token for authorization.
    :param salesman_id: ID of the salesman to add visit record for.
    :return: The visit record data
    """
    logging.debug("Received request to add client visit record by salesman.")
    visit_record_data = request.get_json()
    if not visit_record_data or not all(
            key in visit_record_data for key in ['clientId', 'visitDate', 'notes']):
        logging.error("Missing required fields in request visit_record_data.")
        return jsonify({'msg': 'Faltan campos requeridos.'}), 400

    logging.debug("Adding client visit record from BFF Mobile.")
    adapter = ClientVisitRecordsAdapter()
    return adapter.add_client_visit_record(jwt, salesman_id, visit_record_data)