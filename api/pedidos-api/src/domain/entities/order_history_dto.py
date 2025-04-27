from datetime import datetime


class OrderHistoryDTO:
    def __init__(self, id: str, order_id: str, status: str, description: str, date: datetime):
        """
        Order History Data Transfer Object (DTO) for transferring order history data between layers.
        :param id:
        :param order_id:
        :param status:
        :param description:
        :param date:
        """
        self.id = id
        self.order_id = order_id
        self.status = status
        self.description = description
        self.date = date

    def __repr__(self):
        """
        String representation of the OrderHistoryDTO.
        :return:
        """
        return f"OrderHistoryDTO(id={self.id}, order_id={self.order_id}, status={self.status}, description={self.description}, date={self.date})"

    def to_dict(self):
        """
        Convert the OrderHistoryDTO to a dictionary representation.
        :return:
        """
        return {
            "id": self.id,
            "orderId": self.order_id,
            "status": self.status,
            "description": self.description,
            "date": self.date.isoformat()
        }
