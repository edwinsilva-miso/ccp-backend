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
    if not data or not all(key in data for key in ['user_id', 'title', 'description']):
        logging.error("missing required fields in request data: %s", data)
        raise ValidationApiError

    logging.debug("starting selling plan creation process with data: %s", data)
    selling_plan = SellingPlanDTO(
        id=None,
        user_id=data['user_id'],
        title=data['title'],
        description=data['description'],
        target_amount=data.get('target_amount'),
        target_date=data.get('target_date'),
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
    if not data or not all(key in data for key in ['user_id', 'title', 'description']):
        logging.error("Missing required fields in request data.")
        raise ValidationApiError

    logging.debug("starting selling plan update process for plan_id: %s with data: %s", plan_id, data)
    selling_plan = SellingPlanDTO(
        id=plan_id,
        user_id=data['user_id'],
        title=data['title'],
        description=data['description'],
        target_amount=data.get('target_amount'),
        target_date=data.get('target_date'),
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
        logging.error("missing plan id in request")
        raise ValidationApiError

    logging.debug("starting selling plan retrieval process for plan_id: %s", plan_id)
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
        logging.error("missing user id in request")
        raise ValidationApiError

    logging.debug("starting selling plans retrieval process for user_id: %s", user_id)
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

    logging.debug("starting selling plan deletion process for plan_id: %s", plan_id)
    try:
        use_case = DeleteSellingPlan(selling_plan_adapter)
        result = use_case.execute(plan_id)
        return jsonify({"success": result}), 200
    except ResourceNotFoundError:
        raise ResourceNotFoundError