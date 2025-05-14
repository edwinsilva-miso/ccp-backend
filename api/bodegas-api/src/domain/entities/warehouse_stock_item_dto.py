class WarehouseStockItemDTO:
    """
    Data Transfer Object for Warehouse Stock Item.
    """

    def __init__(self, warehouse_stock_item_id: str | None, warehouse_id: str, item_id: str, bar_code: str = None,
                 identification_code: str = None, width: float = None, height: float = None,
                 depth: float = None, weight: float = None, hallway: str = None,
                 shelf: str = None, sold: bool = False, status: str = "active",
                 created_at: str = None, updated_at: str = None):
        """
        Initialize a new WarehouseStockItemDTO.

        :param warehouse_stock_item_id: Unique identifier for the warehouse stock item
        :param warehouse_id: ID of the warehouse where the item is stored
        :param item_id: ID of the abstract product this item represents
        :param bar_code: Barcode of the item (if available)
        :param identification_code: Alternative identification code if barcode is not available
        :param width: Width of the item in cm
        :param height: Height of the item in cm
        :param depth: Depth of the item in cm
        :param weight: Weight of the item in kg
        :param hallway: Hallway location in the warehouse
        :param shelf: Shelf location in the warehouse
        :param sold: Whether the item has been sold
        :param status: Status of the item (active, damaged, reserved, etc.)
        :param created_at: Creation timestamp
        :param updated_at: Last update timestamp
        """
        self.warehouse_stock_item_id = warehouse_stock_item_id
        self.warehouse_id = warehouse_id
        self.item_id = item_id
        self.bar_code = bar_code
        self.identification_code = identification_code
        self.width = width
        self.height = height
        self.depth = depth
        self.weight = weight
        self.hallway = hallway
        self.shelf = shelf
        self.sold = sold
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return f"WarehouseStockItemDTO(warehouse_stock_item_id={self.warehouse_stock_item_id}, warehouse_id={self.warehouse_id}, " \
               f"item_id={self.item_id}, bar_code={self.bar_code}, " \
               f"identification_code={self.identification_code}, dimensions=[{self.width}x{self.height}x{self.depth}], " \
               f"weight={self.weight}, hallway={self.hallway}, shelf={self.shelf}, " \
               f"sold={self.sold}, status={self.status})"

    def to_dict(self):
        """
        Convert the DTO to a dictionary.
        :return: Dictionary representation of the DTO.
        """
        return {
            "warehouse_stock_item_id": self.warehouse_stock_item_id,
            "warehouse_id": self.warehouse_id,
            "item_id": self.item_id,
            "bar_code": self.bar_code,
            "identification_code": self.identification_code,
            "width": self.width,
            "height": self.height,
            "depth": self.depth,
            "weight": self.weight,
            "hallway": self.hallway,
            "shelf": self.shelf,
            "sold": self.sold,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }