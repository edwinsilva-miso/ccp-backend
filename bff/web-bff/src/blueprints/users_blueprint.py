import logging
from flask import Blueprint, jsonify, request

from ..adapters.users_adapter import UsersAdapter

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)
logger = logging.getLogger(__name__)

users_blueprint = Blueprint('users', __name__, url_prefix='/bff/v1/web/users')

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