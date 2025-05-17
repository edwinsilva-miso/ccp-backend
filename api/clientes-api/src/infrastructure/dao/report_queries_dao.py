import os
from datetime import datetime
from pathlib import Path

from sqlalchemy import text

from ..database.declarative_base import Session

class ReportQueriesDao:

    def __init__(self):
        self.session = Session()
        self.queries_dir = Path(__file__).parent.parent / "resources" / "queries"
        os.makedirs(self.queries_dir, exist_ok=True)

    def get_monthly_product_sales(self, start_date, end_date):
        """
        Get monthly product sales report using native SQL.

        :param start_date: Start date for the report in format 'YYYY-MM-DD'
        :param end_date: End date for the report in format 'YYYY-MM-DD'
        :return: Dictionary with report data containing product sales information
        """
        try:
            # Read SQL query from file
            query_path = self.queries_dir / "monthly_product_sales.sql"
            with open(query_path, 'r') as query_file:
                query = query_file.read()

            # Execute query with parameters
            result = self.session.execute(
                text(query),
                {"start_date": start_date, "end_date": end_date}
            )

            # Convert results to list of dictionaries
            report_data = []
            for row in result:
                report_data.append({
                    "product_id": row[0],
                    "total_quantity": row[1],
                    "total_sales": row[2]
                })

            # Create report metadata
            report_metadata = {
                "report_type": "monthly_product_sales",
                "filters": {
                    "start_date": start_date,
                    "end_date": end_date
                },
                "generated_at": datetime.now().isoformat(),
                "total_records": len(report_data),
                "headers": "Product ID,Total Quantity,Total Sales",
                "data": report_data
            }

            return report_metadata

        except Exception as e:
            self.session.rollback()
            raise Exception(f"Error generating monthly product sales report: {str(e)}")

    def get_monthly_sales(self, start_date, end_date):
        """
        Get monthly sales report using native SQL.

        :param start_date: Start date for the report in format 'YYYY-MM-DD'
        :param end_date: End date for the report in format 'YYYY-MM-DD'
        :return: Dictionary with report data containing sales information
        """
        try:
            # Read SQL query from file
            query_path = self.queries_dir / "monthly_sales.sql"
            with open(query_path, 'r') as query_file:
                query = query_file.read()

            # Execute query with parameters
            result = self.session.execute(
                text(query),
                {"start_date": start_date, "end_date": end_date}
            )

            # Convert results to list of dictionaries
            report_data = []
            for row in result:
                report_data.append({
                    "order_id": row[0],
                    "created_at": row[1],
                    "quantity": row[2],
                    "subtotal": row[3],
                    "tax": row[4],
                    "total": row[5],
                    "currency": row[6],
                    "status": row[7]
                })

            # Create report metadata
            report_metadata = {
                "report_type": "monthly_sales",
                "filters": {
                    "start_date": start_date,
                    "end_date": end_date
                },
                "generated_at": datetime.now().isoformat(),
                "total_records": len(report_data),
                "headers": "Order ID,Created At,Quantity,Subtotal,Tax,Total,Currency,Status",
                "data": report_data
            }

            return report_metadata

        except Exception as e:
            self.session.rollback()
            raise Exception(f"Error generating monthly sales report: {str(e)}")

    def get_sales_per_salesman(self, start_date, end_date, salesman_id):
        """
        Get sales per salesman report using native SQL.

        :param start_date: Start date for the report in format 'YYYY-MM-DD'
        :param end_date: End date for the report in format 'YYYY-MM-DD'
        :param salesman_id: Salesman ID to filter the report
        :return: Dictionary with report data containing sales information
        """
        try:
            # Read SQL query from file
            query_path = self.queries_dir / "sales_per_salesman_id.sql"
            with open(query_path, 'r') as query_file:
                query = query_file.read()

            # Execute query with parameters
            result = self.session.execute(
                text(query),
                {"start_date": start_date, "end_date": end_date, "salesman_id": salesman_id}
            )

            # Convert results to list of dictionaries
            report_data = []
            for row in result:
                report_data.append({
                    "order_id": row[0],
                    "created_at": row[1],
                    "quantity": row[2],
                    "subtotal": row[3],
                    "tax": row[4],
                    "total": row[5],
                    "currency": row[6],
                    "status": row[7]
                })

            # Create report metadata
            report_metadata = {
                "report_type": "sales_per_salesman",
                "filters": {
                    "start_date": start_date,
                    "end_date": end_date,
                    "salesman_id": salesman_id
                },
                "generated_at": datetime.now().isoformat(),
                "total_records": len(report_data),
                "headers": "Order ID,Created At,Quantity,Subtotal,Tax,Total,Currency,Status",
                "data": report_data
            }

            return report_metadata

        except Exception as e:
            self.session.rollback()
            raise Exception(f"Error generating sales per salesman report: {str(e)}")