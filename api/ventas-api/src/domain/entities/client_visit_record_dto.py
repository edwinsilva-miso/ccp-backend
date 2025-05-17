class ClientVisitRecordDTO:
    """
    Data Transfer Object (DTO) for Client Visit Record.
    """

    def __init__(self, record_id: str, client_id: str, salesman_id: str, visit_date: str, notes: str):
        """
        Initialize a ClientVisitRecord instance.
        :param record_id: Unique identifier for the visit record.
        :param client_id: Unique identifier for the client.
        :param salesman_id: Unique identifier for the salesman.
        :param visit_date: Date of the visit.
        :param notes: Notes or comments about the visit.
        """
        self.record_id = record_id
        self.client_id = client_id
        self.salesman_id = salesman_id
        self.visit_date = visit_date
        self.notes = notes

    def __repr__(self):
        return f"ClientVisitRecord(record_id={self.record_id}, client_id={self.client_id}, salesman_id={self.salesman_id} visit_date={self.visit_date}, notes={self.notes})"

    def to_dict(self):
        """
        Convert the ClientVisitRecord to a dictionary.
        :return: Dictionary representation of the ClientVisitRecord.
        """
        return {
            "recordId": self.record_id,
            "clientId": self.client_id,
            "salesmanId": self.salesman_id,
            "visitDate": self.visit_date,
            "notes": self.notes
        }
