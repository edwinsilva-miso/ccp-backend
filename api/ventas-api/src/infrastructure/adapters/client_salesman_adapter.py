from ..dao.client_salesman_dao import ClientSalesmanDAO
from ..mapper.client_salesman_mapper import ClientSalesmanMapper
from ...domain.entities.client_salesman_dto import ClientSalesmanDTO
from ...domain.repositories.client_salesman_repository import ClientSalesmanRepository


class ClientSalesmanAdapter(ClientSalesmanRepository):
    """
    Adapter for ClientSalesmanRepository to interact with ClientSalesmanDAO and ClientSalesmanMapper.
    """

    def get_clients_salesman(self, salesman_id: str) -> list[ClientSalesmanDTO]:
        """
        Retrieves all clients for a given salesman.
        """
        client_salesman_list = ClientSalesmanDAO.get_by_salesman_id(salesman_id)
        return ClientSalesmanMapper.to_dto_list(client_salesman_list)

    def get_client_by_id(self, client_id: str) -> ClientSalesmanDTO | None:
        """
        Retrieves a client by its ID.
        """
        client_salesman = ClientSalesmanDAO.get_by_client_id(client_id)
        return ClientSalesmanMapper.to_dto(client_salesman) if client_salesman else None

    def add(self, client_salesman_dto: ClientSalesmanDTO) -> ClientSalesmanDTO:
        """
        Adds a new Client Salesman.
        """
        client_salesman = ClientSalesmanMapper.to_model(client_salesman_dto)
        client_salesman_dao = ClientSalesmanDAO.save(client_salesman)
        return ClientSalesmanMapper.to_dto(client_salesman_dao)
