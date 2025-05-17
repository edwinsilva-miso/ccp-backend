class OrderReportsDTO:
    """
    OrderReportsDTO is a Data Transfer Object (DTO) that represents the response structure for reports.
    """
    def __init__(self, report_id: str, user_id: str, report_name: str, report_date: str, url: str):
        """
        Initialize a OrderReportsDTO object with the given parameters.
        :param report_id: The unique identifier of the report.
        :param user_id: The unique identifier of the user associated with the report.
        :param report_name: The name of the report.
        :param report_date: The date of the report.
        :param url: The URL where the report can be accessed.
        """
        self.report_id = report_id
        self.user_id = user_id
        self.report_name = report_name
        self.report_date = report_date
        self.url = url

    def to_dict(self):
        """
        Convert the OrderReportsDTO object to a dictionary.
        """
        return {
            "reportId": self.report_id,
            "userId": self.user_id,
            "reportName": self.report_name,
            "reportDate": self.report_date,
            "url": self.url,
        }
