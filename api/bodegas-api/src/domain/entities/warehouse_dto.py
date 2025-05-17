class WarehouseDTO:
    """
    Data Transfer Object for Warehouse.
    """

    def __init__(self, warehouse_id: str | None, location: str, description: str, name: str, administrator_id: str,
                 status: str = "active", created_at: str = None, updated_at: str = None):
        """
        Initialize a new WarehouseDTO.

        :param warehouse_id: Unique identifier for the warehouse
        :param location: Physical location of the warehouse
        :param description: Detailed description of the warehouse
        :param name: Name of the warehouse
        :param administrator_id: ID of the user who administers this warehouse
        :param status: Status of the warehouse (active, inactive)
        :param created_at: Creation timestamp
        :param updated_at: Last update timestamp
        """
        self.warehouse_id = warehouse_id
        self.location = location
        self.description = description
        self.name = name
        self.administrator_id = administrator_id
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return f"WarehouseDTO(id={self.warehouse_id}, location={self.location}, name={self.name}, " \
               f"description={self.description}, administrator_id={self.administrator_id}, " \
               f"status={self.status}, created_at={self.created_at}, updated_at={self.updated_at})"

    def to_dict(self):
        """
        Convert the DTO to a dictionary.
        :return: Dictionary representation of the DTO.
        """
        return {
            "warehouse_id": self.warehouse_id,
            "location": self.location,
            "description": self.description,
            "name": self.name,
            "administrator_id": self.administrator_id,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }