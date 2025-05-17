import csv
import io
import logging

from ..messaging.producer.products_bulk_producer import ProductsBulkProducer

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)

logger = logging.getLogger(__name__)


class ProductsBulkAdapter:
    def __init__(self):
        self.producer = ProductsBulkProducer()

    def process_file(self, file):
        """
        Process the uploaded CSV file.
        :param file: The uploaded file object.
        :return: A response indicating the result of the processing.
        """
        logger.debug("Beginning file processing...")
        file.stream.seek(0, io.SEEK_END)
        file_size = file.stream.tell()
        file.stream.seek(0)

        # 50MB in bytes
        max_size = 50 * 1024 * 1024
        logger.debug("File size: %s bytes", file_size)

        if file_size > max_size:
            logger.error("File size exceeds the maximum limit of 50MB")
            return {
                "msg": "File size exceeds the maximum limit of 50MB"
            }

        logger.debug("File size is within the limit")
        # Read the CSV file
        logger.debug("Reading the CSV file...")
        products = []
        # Decode the file stream to a text stream
        text_stream = io.TextIOWrapper(file.stream, encoding='utf-8')

        logger.debug("Decoding the file stream...")
        csv_reader = csv.DictReader(text_stream)
        for row in csv_reader:
            products.append(row)
        # Here we would process the products
        logger.debug("Processing the products...")
        self.producer.produce(products)

        logger.debug("Finished processing the file")
        return {
            "message": "File successfully uploaded and processed",
            "productsToProcessed": f"{len(products)} products"
        }
