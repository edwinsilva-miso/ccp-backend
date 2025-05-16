import logging
from datetime import datetime

from ..domain.entities.reports.order_reports_dto import OrderReportsDTO

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)
logger = logging.getLogger(__name__)


class GenerateReports:
    """
    Use case for generating reports.
    """

    def __init__(self, order_reports_repository):
        self.order_reports_repository = order_reports_repository

    def execute(self, report_params: dict) -> dict:
        """
        Generate reports based on the provided parameters.
        :param report_params: Dictionary containing report parameters.
        :return: Dictionary containing the generated report.
        """
        logger.debug("Generating reports for user ID: %s", report_params.get('userId'))

        # Here you would implement the logic to generate the report based on the parameters
        # Generate report according to report type
        report_date = datetime.utcnow().isoformat()
        report_name = report_params.get('type') + '_' + report_date.translate(str.maketrans('', '', ':-')) + '.xlsx'

        report_data = self._generate_report_data(report_params)
        logger.debug(f"Generated report data: {report_name}")

        # Store generated report on GCP Cloud Storage
        self._store_on_remote_directory(report_data, report_name)

        # Create a record to save the report info in the database
        logger.debug("Creating record to save the report info in the database.")
        order_report = OrderReportsDTO(
            report_id=None,
            user_id=report_params.get('userId'),
            report_name=report_name,
            report_date=report_date,
            url='https://example.com/' + report_name,  # Replace with actual URL
        )

        # Save the report record in the database
        logger.debug(f"Saving report record: {order_report}")
        report_record = self.order_reports_repository.add(order_report)

        return {
            'id': report_record.report_id,
            'userId': report_record.user_id,
            'name': report_record.report_name,
            'date': report_record.report_date,
            'url': report_record.url,
            'reportData': report_data
        }

    def _generate_report_data(self, report_params: dict) -> list:
        """
        Generate the report data based on the provided parameters.
        :param report_params: Dictionary containing report parameters.
        :return: List of dictionaries containing the report data.
        """
        # Implement the logic to generate the report data based on the parameters
        # This is a placeholder implementation
        report_type = report_params.get('type')
        if report_type == 'sales':
            return [
                {'product': 'Product A', 'sales': 100},
                {'product': 'Product B', 'sales': 200},
            ]
        elif report_type == 'inventory':
            return [
                {'product': 'Product A', 'stock': 50},
                {'product': 'Product B', 'stock': 30},
            ]
        else:
            logger.warning("Unknown report type: %s", report_type)
        return []

    def _store_on_remote_directory(self, report_data: list, report_name: str) -> None:
        """
        Store the generated report on a remote directory (e.g., GCP Cloud Storage).
        :param report_data: The report data to store.
        :param report_name: The name of the report file.
        :return: None
        """
        # Implement the logic to store the report data on a remote directory
        pass
