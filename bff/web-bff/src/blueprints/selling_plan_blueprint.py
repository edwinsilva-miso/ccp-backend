import logging
from flask import Blueprint, request, jsonify

from ..adapters.selling_plan_adapter import SellingPlanAdapter
from ..utils.commons import validate_token   # Use your decorator like @validate_token

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

selling_plan_blueprint = Blueprint('selling_plan', __name__, url_prefix='/bff/v1/web/selling-plans')


@selling_plan_blueprint.route('', methods=['POST'])
@validate_token
def create_selling_plan(jwt):
    logger.debug("Received request to create selling plan")
    plan_data = request.get_json()
    return SellingPlanAdapter.create_selling_plan(jwt, plan_data)


@selling_plan_blueprint.route('/<plan_id>', methods=['PUT'])
@validate_token
def update_selling_plan(plan_id, jwt):
    logger.debug(f"Received request to update selling plan: {plan_id}")
    plan_data = request.get_json()
    return SellingPlanAdapter.update_selling_plan(jwt, plan_id, plan_data)


@selling_plan_blueprint.route('/<plan_id>', methods=['GET'])
@validate_token
def get_selling_plan(plan_id, jwt):
    logger.debug(f"Received request to get selling plan: {plan_id}")
    return SellingPlanAdapter.get_selling_plan(jwt, plan_id)


@selling_plan_blueprint.route('/user/<user_id>', methods=['GET'])
@validate_token
def get_selling_plans_by_user(user_id, jwt):
    logger.debug(f"Received request to get selling plans by user: {user_id}")
    return SellingPlanAdapter.get_selling_plans_by_user(jwt, user_id)


@selling_plan_blueprint.route('/<plan_id>', methods=['DELETE'])
@validate_token
def delete_selling_plan(plan_id, jwt):
    logger.debug(f"Received request to delete selling plan: {plan_id}")
    return SellingPlanAdapter.delete_selling_plan(jwt, plan_id)
