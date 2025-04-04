import logging
from flask import Blueprint, jsonify, request

from ..adapters.users_adapter import UsersAdapter

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)
logger = logging.getLogger(__name__)

users_blueprint = Blueprint('users', __name__, url_prefix='/bff/v1/mobile/users')

@users_blueprint.route('/', methods=['POST'])
def create_user():
    logging.debug("Received request to create user.")
    user_data = request.get_json()
    if not user_data or not all(key in user_data for key in ('name', 'phone', 'email', 'password', 'role')):
        logging.error("Missing required fields in request user_data.")
        return jsonify({'msg': 'Faltan campos requeridos.'}), 400

    logging.debug("Sending information to create new user from BFF Web.")
    adapter = UsersAdapter()
    return adapter.create_user(user_data)

@users_blueprint.route('/auth', methods=['POST'])
def authorize_user():
    logging.debug("Received request to authorize user.")
    auth_data = request.get_json()
    if not auth_data or not all(key in auth_data for key in ('email', 'password')):
        logging.error("Missing required fields in request auth_data.")
        return jsonify({'msg': 'Faltan campos requeridos.'}), 400

    logging.debug("Sending information to authorize user from BFF Web.")
    adapter = UsersAdapter()
    return adapter.authorize(auth_data['email'], auth_data['password'])

@users_blueprint.route('/me', methods=['GET'])
def get_user_info():
    logging.debug("Received request to get user info.")
    token = request.headers.get('Authorization')
    if not token:
        logging.error("Missing Authorization header.")
        return jsonify({'msg': 'Unauthorized'}), 401

    logging.debug("Sending information to get user info from BFF Web.")
    adapter = UsersAdapter()
    return adapter.get_user_info(token)