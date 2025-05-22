from abc import ABC, abstractmethod

from ..entities.order_dto import OrderDTO


class OrderDTORepository(ABC):
    """
    Abstract base class for Order Data Transfer Object (DTO) repository.
    This class defines the interface for the repository, which is responsible for
    managing the persistence of OrderDTO objects.
    """

    @abstractmethod
    def create_order(self, order_dto: OrderDTO) -> OrderDTO | None:
        """
        Create a new order.
        :param order_dto: The OrderDTO object to be created.
        :return: The created OrderDTO object.
        """
        pass

    @abstractmethod
    def get_order(self, order_id: str) -> OrderDTO | None:
        """
        Retrieve an order by its ID.
        :param order_id: The ID of the order to retrieve.
        :return: The OrderDTO object if found, None otherwise.
        """
        pass

    @abstractmethod
    def get_orders_by_client(self, client_id: str) -> list[OrderDTO]:
        """
        Retrieve an order by client ID.
        :param client_id: The ID of the client whose order to retrieve.
        :return: The OrderDTO object if found, None otherwise.
        """
        pass

    @abstractmethod
    def update_order(self, order_dto: OrderDTO) -> OrderDTO | None:
        """
        Update an existing order.
        :param order_dto: The OrderDTO object to be updated.
        :return: The updated OrderDTO object.
        """
        pass

    @abstractmethod
    def list_orders(self) -> list[OrderDTO]:
        """
        List all orders.
        :return: A list of OrderDTO objects.
        """
        pass
