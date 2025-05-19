import logging
import functools

from flask import Blueprint, request, jsonify

from ..adapters.recommendations_adapter import RecommendationsAdapter

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

recommendation_blueprint = Blueprint('recommendations', __name__, url_prefix='/bff/v1/mobile/recommendations')

def token_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            logger.error("Missing Authorization header.")
            return jsonify({'msg': 'Unauthorized'}), 401

        jwt = token.split('Bearer ')[-1] if 'Bearer ' in token else token
        kwargs['jwt'] = jwt
        return f(*args, **kwargs)

    return decorated_function

@recommendation_blueprint.route('', methods=['GET'])
@token_required
def get_all_recommendations(jwt):
    logger.debug("Received request to get all recommendations.")
    logger.debug("Retrieving all recommendations from BFF Web.")
    adapter = RecommendationsAdapter()
    return adapter.get_all_recommendations(jwt)

@recommendation_blueprint.route('', methods=['POST'])
@token_required
def make_recommendation(jwt):
    logger.debug("Received request to make a new recommendation.")
    logger.debug("Making a new recommendation in BFF Web.")
    adapter = RecommendationsAdapter()
    recommendation_data = request.get_json()
    return adapter.make_recommendation(jwt, recommendation_data)