from abc import ABC, abstractmethod
from ..entities.client_visit_record_dto import ClientVisitRecordDTO

class ClientVisitRecordRepository(ABC):
    """
    Abstract base class for Client Visit Record repository.
    This class defines the interface for interacting with the client visit records data source.
    """

    @abstractmethod
    def add_visit_record(self, record: ClientVisitRecordDTO) -> str:
        """
        Add a new client visit record.
        :param record: The ClientVisitRecordDTO object to be added.
        :return: The ID of the newly created visit record.
        """
        pass

    @abstractmethod
    def get_visit_record(self, record_id: str) -> ClientVisitRecordDTO:
        """
        Retrieve a client visit record by its ID.
        :param record_id: The ID of the visit record to retrieve.
        :return: The ClientVisitRecordDTO object corresponding to the given ID.
        """
        pass

    @abstractmethod
    def get_visit_records_by_salesman(self, salesman_id: str) -> list[ClientVisitRecordDTO]:
        """
        Retrieve all visit records for a specific salesman.
        :param salesman_id: The ID of the salesman whose visit records are to be retrieved.
        :return: A list of ClientVisitRecordDTO objects for the specified salesman.
        """
        pass