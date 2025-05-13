import json
import logging

from ..entities.product_dto import ProductDTO

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)
logger = logging.getLogger(__name__)


class ProductsJsonMapper:

    @staticmethod
    def from_json_to_dto_list(products_json: dict) -> list[ProductDTO]:
        """
        Converts a JSON object to a list of ProductDTO.
        :param products_json: List of dictionaries containing product data.
        :return: List of ProductDTO objects.
        """
        logger.debug("Begin converting JSON to DTO list...")
        products = []
        # inbound_products = products_json.get('products', [])
        for product_data in products_json:
            try:
                # Parse JSON strings back to dict, only if they're strings
                details = (json.loads(product_data.get('details'))
                           if isinstance(product_data.get('details'), str)
                           else product_data.get('details'))

                logger.debug(f"product_data.images: {product_data.get('images')}")
                images = product_data.get('images').split(',') if isinstance(product_data.get('images'),
                                                                             str) else product_data.get('images')

                logger.debug(f"images: {images}")

                # Create ProductDTO with dictionary unpacking for required fields
                # and explicit handling for processed fields
                product = ProductDTO(
                    id=None,
                    manufacturer_id=product_data.get('manufacturer_id'),
                    name=product_data.get('name'),
                    brand=product_data.get('brand'),
                    description=product_data.get('description'),
                    stock=product_data.get('stock'),
                    details=details,
                    storage_conditions=product_data.get('storage_conditions'),
                    price=product_data.get('price'),
                    currency=product_data.get('currency'),
                    delivery_time=product_data.get('delivery_time'),
                    images=images,
                    created_at=None,
                    updated_at=None
                )
                products.append(product)
            except Exception as e:
                # Skip invalid products rather than failing the entire batch
                logger.error(f"Error processing product data: {product_data}. Error: {e}")
                print(f"Error processing product data: {e}")
                continue

        return products
