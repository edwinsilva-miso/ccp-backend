from ..database.declarative_base import Session
from ..model.client_salesman_model import ClientSalesmanModel


class ClientSalesmanDAO:
    """
    Data Access Object (DAO) for ClientSalesmanModel.
    Provides an interface to interact with the database.
    """

    @classmethod
    def save(cls, client_salesman: ClientSalesmanModel) -> ClientSalesmanModel:
        """
        Create a new client salesman record in the database.
        :param client_salesman: ClientSalesmanModel to save.
        :return: The saved ClientSalesmanModel with its ID.
        """
        session = Session()
        session.add(client_salesman)
        session.commit()
        session.refresh(client_salesman)
        session.close()
        return client_salesman

    @classmethod
    def get_by_client_id(cls, client_id: str) -> ClientSalesmanModel | None:
        """
        Get a client salesman record by client ID.
        :param client_id: ID of the client to retrieve.
        :return: ClientSalesmanModel if found, None otherwise.
        """
        session = Session()
        client_salesman = session.query(ClientSalesmanModel).filter(ClientSalesmanModel.client_id == client_id).first()
        session.close()
        return client_salesman

    @classmethod
    def get_by_salesman_id(cls, salesman_id: str) -> list[ClientSalesmanModel]:
        """
        Get all client salesman records by salesman ID.
        :param salesman_id: ID of the salesman to retrieve
        :return: List of ClientSalesmanModel with the specified salesman ID.
        """
        session = Session()
        client_salesmen = session.query(ClientSalesmanModel).filter(
            ClientSalesmanModel.salesman_id == salesman_id).all()
        session.close()
        return client_salesmen
