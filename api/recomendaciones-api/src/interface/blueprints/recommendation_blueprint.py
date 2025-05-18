import logging

from flask import Blueprint, jsonify, request

from ..decorator.token_decorator import token_required
from ...application.get_all_recommendations import GetAllRecommendations
from ...application.make_recommendation import MakeRecommendation
from ...infrastructure.adapters.recommendation_adapter import RecommendationAdapter

recommendations_blueprint = Blueprint('recommendations', __name__, url_prefix='/api/v1/recommendations')

recommendations_adapter = RecommendationAdapter()


@recommendations_blueprint.route('/', methods=['POST'])
@token_required(['DIRECTIVO'])
def make_recommendation():
    """
    Endpoint to make a recommendation.
    :return: The recommendation result
    """
    data = request.get_json()
    logging.debug("Received data for recommendation: %s", data)
    use_case = MakeRecommendation(recommendations_adapter)
    recommendation_result = use_case.execute(data)

    return jsonify(recommendation_result.to_dict()), 201


@recommendations_blueprint.route('/', methods=['GET'])
@token_required(['DIRECTIVO'])
def get_all_recommendations():
    """
    Endpoint to get all recommendations.
    :return: List of all recommendations
    """
    use_case = GetAllRecommendations(recommendations_adapter)
    recommendations = use_case.execute()

    return jsonify([recommendation.to_dict() for recommendation in recommendations]), 200
