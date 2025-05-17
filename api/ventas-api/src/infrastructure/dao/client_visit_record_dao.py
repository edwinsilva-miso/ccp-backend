from ..database.declarative_base import Session
from ..model.client_visit_record_model import ClientVisitRecordModel


class ClientVisitRecordDAO:
    """
    Data Access Object (DAO) for Client Visit Record.
    This class provides methods to interact with the client visit records in the database.
    """

    @classmethod
    def save(cls, record: ClientVisitRecordModel) -> str:
        """
        Add a new client visit record to the database.
        :param record: The ClientVisitRecordModel object to be added.
        """
        session = Session()
        session.add(record)
        session.commit()
        session.refresh(record)
        session.close()
        return record.id

    @classmethod
    def get_by_id(cls, record_id: str) -> ClientVisitRecordModel:
        """
        Retrieve a client visit record by its ID.
        :param record_id: The ID of the visit record to retrieve.
        :return: The ClientVisitRecordModel object corresponding to the given ID.
        """
        session = Session()
        record = session.query(ClientVisitRecordModel).filter(ClientVisitRecordModel.id == record_id).first()
        session.close()
        return record

    @classmethod
    def get_by_salesman(cls, salesman_id: str) -> list[ClientVisitRecordModel]:
        """
        Retrieve all visit records for a specific salesman.
        :param salesman_id: The ID of the salesman whose visit records are to be retrieved.
        :return: A list of ClientVisitRecordModel objects for the specified salesman.
        """
        session = Session()
        records = session.query(ClientVisitRecordModel).filter(ClientVisitRecordModel.salesman_id == salesman_id).all()
        session.close()
        return records
