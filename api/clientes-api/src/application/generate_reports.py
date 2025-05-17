import logging
import uuid
from datetime import datetime

from .utils.upload_to_storage import UploadToStorage
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

        # Store generated report on Cloud Storage
        logger.debug("Storing report on remote directory...")
        upload_to_storage = UploadToStorage()
        report_url = upload_to_storage.upload_report(
            file_name=report_name,
            headers=report_headers,
            data=report_data
        )
        logger.debug(f"Report uploaded to: {report_url}")

        # Create a record to save the report info in the database
        logger.debug("Creating record to save the report info in the database.")
        order_report = OrderReportsDTO(
            report_id=str(uuid.uuid4()),
            user_id=data.get('userId'),
            report_name=report_name,
            report_date=report_date,
            url=report_url
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

