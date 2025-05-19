import logging

from flask import Blueprint, jsonify, request

from ..decorators.token_decorator import token_required
from ...application.add_client_visit import AddClientVisit
from ...application.errors.errors import ValidationApiError
from ...application.get_client_visit_record import GetClientVisitRecord
from ...application.get_visits_by_salesman import GetVisitsBySalesman
from ...domain.entities.client_visit_record_dto import ClientVisitRecordDTO
from ...infrastructure.adapters.client_visit_record_adapter import ClientVisitRecordAdapter

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)

client_visit_record_adapter = ClientVisitRecordAdapter()

client_visit_record_blueprint = Blueprint('client_visit_record', __name__, url_prefix='/api/v1/salesman')


@client_visit_record_blueprint.route('<salesman_id>/visits', methods=['GET'])
@token_required(['VENDEDOR', 'DIRECTIVO'])
def get_visits_by_salesman(salesman_id):
    """
    Endpoint to get all visits associated with a salesman.
    """
    if not salesman_id:
        logging.error("Missing salesman ID in request.")
        raise ValidationApiError

    logging.debug("Starting visit retrieval process...")
    use_case = GetVisitsBySalesman(client_visit_record_adapter)
    visits = use_case.execute(salesman_id)
    return jsonify([visit.to_dict() for visit in visits]), 200


@client_visit_record_blueprint.route('<salesman_id>/visits', methods=['POST'])
@token_required(['VENDEDOR', 'DIRECTIVO'])
def add_client_visit(salesman_id):
    """
    Endpoint to add a client visit record.
    """
    # Check if salesman_id is provided
    if not salesman_id:
        logging.error("Missing salesman ID in request.")
        raise ValidationApiError

    data = request.get_json()
    # Check if required fields are present in the request data
    if not data or not all(key in data for key in ['clientId', 'visitDate', 'notes']):
        logging.error("Missing required fields in request data.")
        raise ValidationApiError

    logging.debug("Starting client visit addition process...")
    client_visit_record = ClientVisitRecordDTO(
        record_id=None,
        client_id=data['clientId'],
        salesman_id=salesman_id,
        visit_date=data['visitDate'],
        notes=data['notes']
    )
    use_case = AddClientVisit(client_visit_record_adapter)
    record_id = use_case.execute(client_visit_record)
    return jsonify({'id': record_id}), 201


@client_visit_record_blueprint.route('<salesman_id>/visits/<record_id>', methods=['GET'])
@token_required(['VENDEDOR', 'DIRECTIVO'])
def get_client_visit_record(salesman_id, record_id):
    """
    Endpoint to get a specific client visit record.
    """
    if not salesman_id or not record_id:
        logging.error("Missing salesman ID or record ID in request.")
        raise ValidationApiError

    logging.debug("Starting client visit record retrieval process...")
    use_case = GetClientVisitRecord(client_visit_record_adapter)
    visit_record = use_case.execute(record_id)
    return jsonify(visit_record.to_dict()), 200
