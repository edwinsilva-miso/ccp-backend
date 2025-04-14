import logging
from flask import Blueprint, jsonify, request

from ...application.errors.errors import ValidationApiError
from ...application.create_provider import CreateProvider
from ...application.update_provider import UpdateProvider
from ...application.get_all_providers import GetAllProviders
from ...application.get_provider_by_id import GetProviderById
from ...application.get_provider_by_nit import GetProviderByNit
from ...application.delete_provider import DeleteProvider
from ...domain.entities.provider_dto import ProviderDTO
from ...infrastructure.adapters.provider_adapter import ProviderAdapter

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)
logger = logging.getLogger(__name__)

providers_blueprint = Blueprint('providers', __name__, url_prefix='/api/v1/providers')

providers_adapter = ProviderAdapter()

@providers_blueprint.route('/', methods=['POST'])
def create_provider():
    data = request.get_json()
    if not data or not all(key in data for key in ('name', 'phone', 'email', 'nit', 'legal_representative', 'country')):
        logging.error("Missing required fields in request data.")
        raise ValidationApiError

    provider = ProviderDTO(
        id=None,
        nit=data['nit'],
        name=data['name'],
        address=data['address'],
        phone=data['phone'],
        email=data['email'],
        legal_representative=data['legal_representative'],
        country=data['country'],
        status=None,
        created=None,
        updated=None
    )
    use_case = CreateProvider(providers_adapter)
    provider_id = use_case.execute(provider)
    return jsonify({'id': provider_id}), 201

@providers_blueprint.route('/', methods=['GET'])
def get_all_providers():
    use_case = GetAllProviders(providers_adapter)
    providers = use_case.execute()
    return jsonify([provider.__dict__ for provider in providers]), 200


@providers_blueprint.route('/<string:provider_id>', methods=['GET'])
def get_provider_by_id(provider_id):
    use_case = GetProviderById(providers_adapter)
    provider = use_case.execute(provider_id)
    return jsonify(provider.__dict__), 200


@providers_blueprint.route('/search', methods=['GET'])
def get_provider_by_nit():
    nit = request.args.get('nit')
    if not nit:
        logging.error("Missing 'nit' query parameter.")
        raise ValidationApiError

    use_case = GetProviderByNit(providers_adapter)
    provider = use_case.execute(nit)
    return jsonify(provider.__dict__), 200

@providers_blueprint.route('/<string:provider_id>', methods=['PUT'])
def update_provider(provider_id):
    data = request.get_json()
    if not data or not all(key in data for key in ('name', 'address', 'phone', 'email', 'legal_representative', 'country', 'status')):
        logging.error("Missing required fields in request data.")
        raise ValidationApiError

    provider = ProviderDTO(
        id=None,
        nit=None,
        name=data['name'],
        address=data['address'],
        phone=data['phone'],
        email=data['email'],
        legal_representative=data['legal_representative'],
        country=data['country'],
        status=data['status'],
        created=None,
        updated=None
    )
    use_case = UpdateProvider(providers_adapter)
    updated = use_case.execute(provider_id, provider)
    return jsonify(updated.__dict__), 200

@providers_blueprint.route('/<string:provider_id>', methods=['DELETE'])
def delete_provider(provider_id):
    use_case = DeleteProvider(providers_adapter)
    use_case.execute(provider_id)
    return {}, 204



