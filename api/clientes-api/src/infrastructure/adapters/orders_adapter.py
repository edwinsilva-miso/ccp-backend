from ..dao.order_dao import OrderDAO
from ..mapper.order_mapper import OrderMapper
from ...domain.entities.order_dto import OrderDTO
from ...domain.repositories.orders_repository import OrdersRepository


class OrdersAdapter(OrdersRepository):
    """
    Adapter class to interact with the OrderDAO and convert between OrderDTO and OrderModel.
    """

    def get_orders_by_client(self, client_id: str) -> list[OrderDTO]:
        return OrderMapper.to_dto_single_list(OrderDAO.find_by_client_id(client_id))

    def get_by_id(self, id: str) -> OrderDTO | None:
        order = OrderDAO.get_order_by_id(id)
        return OrderMapper.to_dto(order) if order else None

    def add(self, order: OrderDTO) -> OrderDTO | None:
        order_id = OrderDAO.save(OrderMapper.to_model(order))
        returned = OrderDAO.get_order_by_id(order_id)
        return OrderMapper.to_dto(returned) if returned else None

    def update(self, order: OrderDTO) -> OrderDTO | None:
        updated = OrderDAO.update(OrderMapper.to_model(order))
        return OrderMapper.to_dto(updated) if updated else None
