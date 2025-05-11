import logging

from flask import Blueprint, request, jsonify

from ..decorators.token_decorator import token_required
from ...application.create_selling_plan import CreateSellingPlan
from ...application.update_selling_plan import UpdateSellingPlan
from ...application.get_selling_plan_by_id import GetSellingPlanById
from ...application.get_selling_plans_by_user_id import GetSellingPlansByUserId
from ...application.delete_selling_plan import DeleteSellingPlan
from ...application.errors.errors import ValidationApiError, ResourceNotFoundError
from ...domain.entities.selling_plan_dto import SellingPlanDTO
from ...infrastructure.adapters.selling_plan_adapter import SellingPlanAdapter

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

selling_plan_adapter = SellingPlanAdapter()

selling_plan_blueprint = Blueprint('selling_plan', __name__, url_prefix='/api/v1/selling-plans')


@selling_plan_blueprint.route('', methods=['POST'])
@token_required(['VENDEDOR'])
def create_selling_plan():
    """
    Endpoint to create a new selling plan.
    """
    data = request.get_json()
    if not data or not all(key in data for key in ['userId', 'title', 'description']):
        logging.error("Missing required fields in request data.")
        raise ValidationApiError

    logging.debug("Starting selling plan creation process...")
    selling_plan = SellingPlanDTO(
        id=None,
        user_id=data['userId'],
        title=data['title'],
        description=data['description'],
        target_amount=data.get('targetAmount'),
        target_date=data.get('targetDate'),
        status=data.get('status', 'active')
    )
    use_case = CreateSellingPlan(selling_plan_adapter)
    response = use_case.execute(selling_plan)
    return jsonify(response.to_dict()), 201


@selling_plan_blueprint.route('/<plan_id>', methods=['PUT'])
@token_required(['VENDEDOR'])
def update_selling_plan(plan_id):
    """
    Endpoint to update an existing selling plan.
    """
    data = request.get_json()
    if not data or not all(key in data for key in ['userId', 'title', 'description']):
        logging.error("Missing required fields in request data.")
        raise ValidationApiError

    logging.debug("Starting selling plan update process...")
    selling_plan = SellingPlanDTO(
        id=plan_id,
        user_id=data['userId'],
        title=data['title'],
        description=data['description'],
        target_amount=data.get('targetAmount'),
        target_date=data.get('targetDate'),
        status=data.get('status', 'active')
    )
    try:
        use_case = UpdateSellingPlan(selling_plan_adapter)
        response = use_case.execute(selling_plan)
        return jsonify(response.to_dict()), 200
    except ResourceNotFoundError:
        raise ResourceNotFoundError


@selling_plan_blueprint.route('/<plan_id>', methods=['GET'])
@token_required(['VENDEDOR'])
def get_selling_plan(plan_id):
    """
    Endpoint to get a selling plan by its ID.
    """
    if not plan_id:
        logging.error("Missing plan ID in request.")
        raise ValidationApiError

    logging.debug("Starting selling plan retrieval process...")
    try:
        use_case = GetSellingPlanById(selling_plan_adapter)
        selling_plan = use_case.execute(plan_id)
        return jsonify(selling_plan.to_dict()), 200
    except ResourceNotFoundError:
        raise ResourceNotFoundError


@selling_plan_blueprint.route('/user/<user_id>', methods=['GET'])
@token_required(['VENDEDOR'])
def get_selling_plans_by_user(user_id):
    """
    Endpoint to get all selling plans for a given user.
    """
    if not user_id:
        logging.error("Missing user ID in request.")
        raise ValidationApiError

    logging.debug("Starting selling plans retrieval process...")
    use_case = GetSellingPlansByUserId(selling_plan_adapter)
    selling_plans = use_case.execute(user_id)
    return jsonify([plan.to_dict() for plan in selling_plans]), 200


@selling_plan_blueprint.route('/<plan_id>', methods=['DELETE'])
@token_required(['VENDEDOR'])
def delete_selling_plan(plan_id):
    """
    Endpoint to delete a selling plan by its ID.
    """
    if not plan_id:
        logging.error("Missing plan ID in request.")
        raise ValidationApiError

    logging.debug("Starting selling plan deletion process...")
    try:
        use_case = DeleteSellingPlan(selling_plan_adapter)
        result = use_case.execute(plan_id)
        return jsonify({"success": result}), 200
    except ResourceNotFoundError:
        raise ResourceNotFoundError