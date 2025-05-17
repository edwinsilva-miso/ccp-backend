import logging
import uuid
from datetime import datetime

from .utils.create_report_file import CreateReportFile
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

    def __init__(self, order_reports_repository, report_queries_adapter):
        self.order_reports_repository = order_reports_repository
        self.report_queries_adapter = report_queries_adapter

    def execute(self, data: dict) -> dict:
        """
        Generate reports based on the provided parameters.
        :param data: Dictionary containing report parameters.
        :return: Dictionary containing the generated report.
        """
        logger.debug("Generating reports for user ID: %s", data.get('userId'))

        # Here you would implement the logic to generate the report based on the parameters
        # Generate report according to report type
        report_date = datetime.utcnow().isoformat()
        report_name = 'CCP_' + data.get('type') + '_' + data.get('userId') + '_' + report_date.translate(
            str.maketrans('', '', ':-')) + '.xlsx'

        report_metadata = self._generate_report_data(data)
        report_data = report_metadata.get('data', [])
        report_headers = report_metadata.get('headers')
        logger.debug(f"Generated report data: {report_name}")

        logger.debug("Creating report file...")
        create_report_file = CreateReportFile(report_name, report_headers, report_data)
        report_file_path = create_report_file.create_file()
        logger.debug(f"Report file created at: {report_file_path}")

        # Store generated report on GCP Cloud Storage
        self._store_on_remote_directory(report_data, report_name)

        # Create a record to save the report info in the database
        logger.debug("Creating record to save the report info in the database.")
        order_report = OrderReportsDTO(
            report_id=str(uuid.uuid4()),
            user_id=data.get('userId'),
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

    def _generate_report_data(self, data: dict) -> dict:
        """
        Generate the report data based on the provided parameters.
        :param data: Dictionary containing report parameters.
        :return: List of dictionaries containing the report data.
        """
        # Implement the logic to generate the report data based on the parameters
        # This is a placeholder implementation
        logger.debug("Generating report data...")
        metadata = {}
        report_type = data.get('type')
        filters = data.get('filters', {})
        logger.debug(f"Report type: {report_type}")
        if report_type == 'VENTAS_POR_MES':
            metadata = self.report_queries_adapter.get_monthly_sales(
                start_date=filters.get('startDate'),
                end_date=filters.get('endDate')
            )
        elif report_type == 'PRODUCTOS_MAS_VENDIDOS':
            metadata = self.report_queries_adapter.get_monthly_product_sales(
                start_date=filters.get('startDate'),
                end_date=filters.get('endDate')
            )
        elif report_type == 'VENTAS_POR_VENDEDOR':
            metadata = self.report_queries_adapter.get_monthly_sales_by_salesman(
                start_date=filters.get('startDate'),
                end_date=filters.get('endDate'),
                salesman_id=filters.get('salesmanId')
            )
        else:
            logger.warning("Unknown report type: %s", report_type)

        logger.debug("Report data generated successfully.")
        return metadata

    def _store_on_remote_directory(self, report_data: list, report_name: str) -> None:
        """
        Store the generated report on a remote directory (e.g., GCP Cloud Storage).
        :param report_data: The report data to store.
        :param report_name: The name of the report file.
        :return: None
        """
        # Implement the logic to store the report data on a remote directory
        pass

    def _generate_file(self, report_name, report_data: dict):

        """
        Generate a file for the report data.
        :param report_name: The name of the report file.
        :param report_data: The report data to store.
        :return: The path to the generated file.
        """
        # Implement the logic to generate a file for the report data

        pass
