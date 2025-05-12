from ..dao.client_visit_record_dao import ClientVisitRecordDAO
from ..mapper.client_visit_record_mapper import ClientVisitRecordMapper
from ...domain.entities.client_visit_record_dto import ClientVisitRecordDTO
from ...domain.repositories.client_visit_record_repository import ClientVisitRecordRepository


class ClientVisitRecordAdapter(ClientVisitRecordRepository):
    """
    Adapter for ClientVisitRecordRepository to interact with ClientVisitRecordDAO and ClientVisitRecordMapper.
    """

    def add_visit_record(self, record: ClientVisitRecordDTO) -> str:
        """
        Add a new client visit record.
        :param record: The ClientVisitRecordDTO object to be added.
        """
        record_model = ClientVisitRecordMapper.to_model(record)
        return ClientVisitRecordDAO.save(record_model)

    def get_visit_record(self, record_id: str) -> ClientVisitRecordDTO:
        """
        Retrieve a client visit record by its ID.
        :param record_id: The ID of the visit record to retrieve.
        :return: The ClientVisitRecordDTO object corresponding to the given ID.
        """
        client_visit_record = ClientVisitRecordDAO.get_by_id(record_id)
        return ClientVisitRecordMapper.to_dto(client_visit_record) if client_visit_record else None

    def get_visit_records_by_salesman(self, salesman_id: str) -> list[ClientVisitRecordDTO]:
        """
        Retrieve all visit records for a specific salesman.
        :param salesman_id: The ID of the salesman whose visit records are to be retrieved.
        :return: A list of ClientVisitRecordDTO objects for the specified salesman.
        """
        client_visit_records = ClientVisitRecordDAO.get_by_salesman(salesman_id)
        return ClientVisitRecordMapper.to_dto_list(client_visit_records) if client_visit_records else []
