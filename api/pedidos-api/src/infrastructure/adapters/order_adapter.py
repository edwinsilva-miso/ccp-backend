from ..dao.orders_dao import OrderDAO
from ..mapper.orders_mapper import OrderMapper
from ...domain.entities.order_dto import OrderDTO
from ...domain.repositories.orders_repository import OrderDTORepository


class OrdersAdapter(OrderDTORepository):

    def create_order(self, order_dto: OrderDTO) -> OrderDTO | None:
        order_id = OrderDAO.save(OrderMapper.to_model(order_dto))
        order_dto = OrderDAO.get_by_id(order_id)
        return OrderMapper.to_dto(order_dto) if order_dto else None

    def get_order(self, order_id: str) -> OrderDTO | None:
        order = OrderDAO.get_by_id(order_id)
        return OrderMapper.to_dto(order) if order else None

    def get_orders_by_client(self, client_id: str) -> list[OrderDTO]:
        return OrderMapper.to_dto_list(OrderDAO.find_by_client_id(client_id))

    def update_order(self, order_dto: OrderDTO) -> OrderDTO | None:
        updated = OrderDAO.update(OrderMapper.to_model(order_dto))
        return OrderMapper.to_dto(updated) if updated else None

    def list_orders(self) -> list[OrderDTO]:
        return OrderMapper.to_dto_list(OrderDAO.find_all())
