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

    def __init__(self, product_repository):
        """
        Initializes the ProcessUpdateProductsStockMessage with a product repository.
        :param product_repository: An instance of ProductRepository.
        """
        self.product_repository = product_repository

    def process(self, message: dict) -> None:
        """
        Process the message.
        """
        # Here you would implement the logic to process the message.
        # For example, updating the stock of products in the database.
        logging.debug(f"Processing message: {message}")
        product_list = message.get("products", [])
        if not product_list:
            logging.error("No products found in the message.")
            return

        for product in product_list:
            product_id = product.get("productId")
            logging.debug(f"Updating stock for product ID: {product_id}")
            existing_product = self.product_repository.get_by_id(product_id)
            if not existing_product:
                logging.error(f"Product with ID {product_id} does not exist.")
                continue

            quantity = product.get("quantity")
            if quantity is None or not isinstance(quantity, int) or quantity <= 0:
                logging.error(f"Invalid quantity for product ID {product_id}. Quantity must be a positive integer.")
                continue
            new_stock = existing_product.stock - quantity
            existing_product.stock = new_stock
            # Update the stock in the repository
            self.product_repository.update(existing_product)
            logging.debug(f"Updated stock for product {product_id} to {new_stock}")

        logging.debug("Message processed successfully.")
