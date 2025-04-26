import logging

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)
logger = logging.getLogger(__name__)


class ProcessUpdateProductsStockMessage:
    """
    Process the update products stock message.
    """

    def process(self, message: dict) -> None:
        """
        Process the message.
        """
        # Here you would implement the logic to process the message.
        # For example, updating the stock of products in the database.
        logging.debug(f"Processing message: {message}")
        # Simulate processing time
        import time
        time.sleep(1)
        logging.debug("Message processed successfully.")
