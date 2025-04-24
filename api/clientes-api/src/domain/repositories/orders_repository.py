from abc import ABC, abstractmethod
from ..entities.order_dto import OrderDTO

class OrdersRepository(ABC):

    @abstractmethod
    def get_orders_by_client(self, client_id: str) -> list[OrderDTO]:
        """Get all orders given a client ID"""
        pass

    @abstractmethod
    def get_by_id(self, id: str) -> OrderDTO | None:
        """Get order by ID"""
        pass

    @abstractmethod
    def add(self, order: OrderDTO) -> OrderDTO | None:
        """Add a new order"""
        pass

    @abstractmethod
    def update(self, order: OrderDTO) -> OrderDTO | None:
        """Update an existing order"""
        pass

