import logging

from flask import Blueprint, request, jsonify

from ..decorators.token_decorator import token_required
from ...application.associate_client import AssociateClient
from ...application.errors.errors import ValidationApiError
from ...application.get_clients_by_salesman import GetClientsBySalesman
from ...domain.entities.client_salesman_dto import ClientSalesmanDTO
from ...infrastructure.adapters.client_salesman_adapter import ClientSalesmanAdapter

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)

client_salesman_adapter = ClientSalesmanAdapter()

client_salesman_blueprint = Blueprint('client_salesman', __name__, url_prefix='/api/v1/salesman')


@client_salesman_blueprint.route('<salesman_id>/clients', methods=['GET'])
@token_required(['VENDEDOR', 'DIRECTIVO'])
def get_clients_by_salesman(salesman_id):
    """
    Endpoint to get all clients associated with a salesman.
    """
    if not salesman_id:
        logging.error("Missing salesman ID in request.")
        raise ValidationApiError

    logging.debug("Starting client retrieval process...")
    use_case = GetClientsBySalesman(client_salesman_adapter)
    clients = use_case.execute(salesman_id)
    return jsonify([client.to_dict() for client in clients]), 200


@client_salesman_blueprint.route('<salesman_id>/clients', methods=['POST'])
@token_required(['VENDEDOR', 'DIRECTIVO'])
def associate_client(salesman_id):
    """
    Endpoint to associate a client with a salesman.
    """
    data = request.get_json()
    if not data or not all(key in data for key in ['client', 'address', 'city', 'country', 'storeName']) or \
            not all(key in data['client'] for key in ['id', 'name', 'phone', 'email']):
        logging.error("Missing required fields in request data.")
        raise ValidationApiError

    logging.debug("Starting client association process...")
    client_salesman = ClientSalesmanDTO(
        id=None,
        client_id=data['client']['id'],
        salesman_id=salesman_id,
        client_name=data['client']['name'],
        client_phone=data['client']['phone'],
        client_email=data['client']['email'],
        address=data['address'],
        city=data['city'],
        country=data['country'],
        store_name=data['storeName']
    )
    use_case = AssociateClient(client_salesman_adapter)
    response = use_case.execute(client_salesman)
    return jsonify(response.to_dict()), 201
