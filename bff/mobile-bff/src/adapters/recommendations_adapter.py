import logging
import os

import requests

from .products_adapter import ProductsAdapter

RECOMMENDATIONS_API_URL = os.environ.get('RECOMMENDATIONS_API_URL', 'http://localhost:5200')

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)

logger = logging.getLogger(__name__)


class RecommendationsAdapter:
    def get_all_recommendations(self, jwt):
        """
        Get all recommendations.
        :param jwt: JWT token for authorization.
        :return: The all recommendations data
        """
        logger.debug("Getting all recommendations")
        headers = {'Authorization': f'Bearer {jwt}'}
        response = requests.get(f"{RECOMMENDATIONS_API_URL}/api/v1/recommendations", headers=headers)
        logger.debug(f"Response received from API: {response.json()}")
        recommendations_data = None
        if response.status_code == 200:
            recommendations_data = response.json()
            for recommendation in recommendations_data:
                recommendation = self._decorate_recommendation_data(jwt, recommendation)
                logger.debug(f"Recommendation decorated: {recommendation}")

        return recommendations_data, response.status_code

    def make_recommendation(self, jwt, recommendation_data):
        """
        Make a new recommendation.
        :param jwt: JWT token for authorization.
        :param recommendation_data: Data for the new recommendation.
        :return: The created recommendation data
        """
        logger.debug("Making a new recommendation")
        headers = {'Authorization': f'Bearer {jwt}'}
        response = requests.post(f"{RECOMMENDATIONS_API_URL}/api/v1/recommendations", json=recommendation_data,
                                 headers=headers)
        logger.debug(f"Response received from API: {response.json()}")
        recommendation_data = None
        if response.status_code == 201:
            recommendation_data = response.json()
            recommendation_data = self._decorate_recommendation_data(jwt, recommendation_data)
            logger.debug(f"Recommendation decorated: {recommendation_data}")

        return recommendation_data, response.status_code

    def _decorate_recommendation_data(self, jwt, recommendation_data):
        """
        Decorate the recommendation with product details.
        :param recommendation_data: The recommendation data
        :return: The decorated recommendation data
        """
        logger.debug(f"Decorating order {recommendation_data['id']}")
        product_adapter = ProductsAdapter()
        product_id = recommendation_data.get('productId')
        product_data, _ = product_adapter.get_product_by_id(jwt, product_id)
        recommendation_data['productName'] = product_data.get('name')

        return recommendation_data
