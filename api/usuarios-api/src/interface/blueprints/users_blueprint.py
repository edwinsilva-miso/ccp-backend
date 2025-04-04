import logging
from flask import Blueprint, jsonify, request

from ...application.errors.errors import ValidationApiError
from ...application.create_user import CreateUser
from ...application.login_user import LoginUser
from ...domain.entities.user_dto import UserDTO
from ...infrastructure.adapters.user_adapter import UserAdapter

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)
logger = logging.getLogger(__name__)

user_blueprint = Blueprint('users', __name__, url_prefix='/api/v1/users')

user_adapter = UserAdapter()

@user_blueprint.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or not all(key in data for key in ('name', 'phone', 'email', 'password', 'role')):
        logging.error("Missing required fields in request data.")
        raise ValidationApiError

    user = UserDTO(
        id=None,
        name=data['name'],
        phone=data['phone'],
        email=data['email'],
        password=data['password'],
        token=None,
        salt=None,
        role=data['role'],
        expire_at=None
    )
    use_case = CreateUser(user_adapter)
    user_id = use_case.execute(user)
    return jsonify({'id': user_id}), 201

@user_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not all(key in data for key in ('email', 'password')):
        logging.error("Missing required fields in request data.")
        raise ValidationApiError


    use_case = LoginUser(user_adapter)
    response = use_case.execute(data['email'], data['password'])
    return jsonify(response), 200