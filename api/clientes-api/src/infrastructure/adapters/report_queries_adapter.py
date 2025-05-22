from ..dao.report_queries_dao import ReportQueriesDao

class ReportQueriesAdapter:
    """
    Adapter for report queries.
    """
    def __init__(self):
        self.report_queries_dao = ReportQueriesDao()

    def get_monthly_product_sales(self, start_date, end_date):
        """
        Get monthly product sales report using native SQL.
        :param start_date: Start date for the report in format 'YYYY-MM-DD'
        :param end_date: End date for the report in format 'YYYY-MM-DD'
        :return: Dictionary with report data containing product sales information
        """
        return self.report_queries_dao.get_monthly_product_sales(start_date, end_date)

    def get_monthly_sales(self, start_date, end_date):
        """
        Get monthly sales report using native SQL.
        :param start_date: Start date for the report in format 'YYYY-MM-DD'
        :param end_date: End date for the report in format 'YYYY-MM-DD'
        :return: Dictionary with report data containing sales information
        """
        return self.report_queries_dao.get_monthly_sales(start_date, end_date)

    def get_monthly_sales_by_salesman(self, start_date, end_date, salesman_id):
        """
        Get monthly sales by salesman report using native SQL.
        :param start_date: Start date for the report in format 'YYYY-MM-DD'
        :param end_date: End date for the report in format 'YYYY-MM-DD'
        :param salesman_id: ID of the salesman
        :return: Dictionary with report data containing sales information by salesman
        """
        return self.report_queries_dao.get_sales_per_salesman(start_date, end_date, salesman_id)