from ..dao.order_reports_dao import OrderReportsDAO
from ..mapper.order_reports_mapper import OrderReportsMapper
from ...domain.entities.reports.order_reports_dto import OrderReportsDTO
from ...domain.repositories.order_reports_repository import OrderReportsRepository


class OrderReportsAdapter(OrderReportsRepository):

    def add(self, dto: OrderReportsDTO) -> OrderReportsDTO:
        order_report = OrderReportsDAO.save(OrderReportsMapper.to_model(dto))
        return OrderReportsMapper.to_dto(order_report)

    def get_by_user_id(self, user_id: str) -> list[OrderReportsDTO]:
        order_reports_list = OrderReportsDAO.get_by_user_id(user_id)
        return OrderReportsMapper.to_dto_list(order_reports_list)
