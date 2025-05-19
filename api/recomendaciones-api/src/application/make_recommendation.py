import json
import logging

from ..domain.entities.recommentation_result_dto import RecommendationResultDTO
from ..domain.service.calculation_sales_service import CalculationSalesService

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)
logger = logging.getLogger(__name__)


class MakeRecommendation:
    """
    Class to handle the recommendation process
    """

    def __init__(self, recommendation_repository):
        """
        Initialize the MakeRecommendation class
        :param recommendation_repository: The repository to handle recommendations
        """
        self.recommendation_repository = recommendation_repository
        self.calculation_sales_service = CalculationSalesService()

    def execute(self, sales_data: dict) -> RecommendationResultDTO:
        """
        Execute the recommendation process
        :param sales_data: A dictionary containing sales data
        :return: The recommendation saved
        """
        logger.debug("Starting the recommendation process")

        # Calculate the optimum quantity
        quantity_to_order = self.calculation_sales_service.calculate_optimum_quantity(sales_data)
        logger.debug("Optimum quantity calculated: %d", quantity_to_order)

        # Prepare data to save
        product = sales_data.get('product')
        projection = sales_data.get('projection')
        events = json.dumps(sales_data.get('events', []))
        recommendation_text = f"La cantidad óptima a comprar para {product.get('name')} y obtener ${projection.get('salesTarget', '0')} {projection.get('currency')} es {quantity_to_order} unidades."

        # Create a recommendation result DTO
        recommendation_result_dto = RecommendationResultDTO(
            id=None,
            product_id=product.get('id'),
            events=events,
            target_sales_amount=projection.get('salesTarget', 0),
            currency=projection.get('currency'),
            recommendation=recommendation_text,
        )

        # Save the recommendation result
        saved_recommendation = self.recommendation_repository.add(recommendation_result_dto)

        logger.info("Recommendation process completed successfully")
        return saved_recommendation
