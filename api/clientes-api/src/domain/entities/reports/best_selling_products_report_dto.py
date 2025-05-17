class BestSellingProductsReportDTO:
    def __init__(self, product_id: int, quantity_sold: int, total_sold: float):
        """
        Initialize a BestSellingProductsReportDTO object with the given parameters.
        :param product_id: The unique identifier of the product.
        :param quantity_sold: The quantity of the product sold.
        :param total_sold: The total amount sold for the product.
        """
        self.product_id = product_id
        self.quantity_sold = quantity_sold
        self.total_sold = total_sold

    def to_dict(self):
        """
        Convert the BestSellingProductsReportDTO object to a dictionary.
        """
        return {
            "productId": self.product_id,
            "quantitySold": self.quantity_sold,
            "totalSold": self.total_sold
        }