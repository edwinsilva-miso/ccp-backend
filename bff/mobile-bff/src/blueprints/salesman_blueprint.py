import functools
import logging

from flask import Blueprint, jsonify, request

from ..adapters.salesman_adapter import SalesmanAdapter

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)
logger = logging.getLogger(__name__)

salesman_blueprint = Blueprint('salesman', __name__, url_prefix='/bff/v1/mobile/salesman')


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


@salesman_blueprint.route('<salesman_id>/clients', methods=['GET'])
@token_required
def get_clients_salesman(jwt, salesman_id):
    logging.debug("Received request to gegt clients by salesman.")
    logging.debug("Retrieving all salesman's clients from BFF Mobile")
    adapter = SalesmanAdapter()
    return adapter.get_clients_by_salesman(jwt, salesman_id)


@salesman_blueprint.route('<salesman_id>/clients', methods=['POST'])
@token_required
def associate_client_salesman(jwt, salesman_id):
    logging.debug("Received request to associate client with salesman.")
    client_data = request.get_json()
    if not client_data or not all(
            key in client_data for key in ['client', 'address', 'city', 'country', 'storeName']) or \
            not all(key in client_data['client'] for key in ['id', 'name', 'phone', 'email']):
        logging.error("Missing required fields in request client_data.")
        return jsonify({'msg': 'Faltan campos requeridos.'}), 400

    logging.debug("Associating client with salesman from BFF Mobile.")
    adapter = SalesmanAdapter()
    return adapter.associate_client(jwt, salesman_id, client_data)
