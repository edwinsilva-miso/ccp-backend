import datetime
import logging

from ..exceptions.recommendation_error import RecommendationError

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)
logger = logging.getLogger(__name__)


class CalculationSalesService:

    def __init__(self):
        """
        Initialize the CalculationSalesService
        """
        pass

    def calculate_optimum_quantity(self, sales_data: dict) -> int:
        """
        Calculate the optimum quantity to order based on sales data
        :param sales_data: A dictionary containing sales data
        :return: The result of the sales calculation
        """
        logger.debug("Starting sales calculation with data: %s", sales_data)
        try:
            product = sales_data.get('product')
            projection = sales_data.get('projection')
            events = sales_data.get('events', [])

            current_stock = product.get('stock', 0)
            sales_target = projection.get('salesTarget', 0)

            # Estimation of future demand (could be a complex calculation)
            project_demand = sales_target

            # Adjustment per events
            events_factor = 1.0
            today = datetime.date.today()
            for event in events:
                event_date = datetime.datetime.strptime(event['date'], '%Y-%m-%d').date()
                days_to_event = (event_date - today).days
                # If the event is in the near future, consider an impact (very simplified)
                if 0 <= days_to_event <= 30:
                    events_factor *= 1.1  # Increase demand by 10% for near future events

            # Calculate the quantity to order
            adjust_demand = int(project_demand * events_factor)
            quantity_to_order = max(0, adjust_demand - current_stock)

            logger.info("Sales calculation completed successfully")
            return quantity_to_order
        except Exception as e:
            logger.error("Error during sales calculation: %s", str(e))
            raise RecommendationError
