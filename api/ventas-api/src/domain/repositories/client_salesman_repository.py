from abc import ABC, abstractmethod

from ..entities.client_salesman_dto import ClientSalesmanDTO


class ClientSalesmanRepository(ABC):
    """
    Port defining the interface for Client Salesman repository.
    """

    @abstractmethod
    def get_clients_salesman(self, salesman_id: str) -> list[ClientSalesmanDTO]:
        """
        Retrieves all clients for a given salesman.
        :param salesman_id: ID of the client
        :return: ClientSalesmanDTO object
        """
        pass

    @abstractmethod
    def get_client_by_id(self, client_id: str) -> ClientSalesmanDTO:
        """
        Retrieves a client by its ID.
        :param client_id: ID of the client
        :return: ClientSalesmanDTO object
        """
        pass

    @abstractmethod
    def add(self, client_salesman_dto: ClientSalesmanDTO) -> ClientSalesmanDTO:
        """
        Adds a new Client Salesman.
        :param client_salesman_dto: ClientSalesmanDTO object to add
        :return: ClientSalesmanDTO object
        """
        pass
