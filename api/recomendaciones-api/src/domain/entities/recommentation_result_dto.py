class RecommendationResultDTO:
    def __init__(self, id: str, product_id: str, events: str, target_sales_amount: float,
                 currency: str, recommendation: str, created_at: str = None):
        """
        Initialize the RecommendationResultDTO with the given parameters.
        :param id: Unique identifier for the recommendation result.
        :param product_id: Unique identifier for the product.
        :param events: Events associated with the recommendation.
        :param target_sales_amount: Target sales amount for the recommendation.
        :param currency: Currency of the target sales amount.
        :param recommendation: Recommendation text.
        """
        self.id = id
        self.product_id = product_id
        self.events = events
        self.target_sales_amount = target_sales_amount
        self.currency = currency
        self.recommendation = recommendation
        self.created_at = created_at

    def to_dict(self):
        """
        Convert the RecommendationResultDTO to a dictionary.
        :return: Dictionary representation of the RecommendationResultDTO.
        """
        return {
            "id": self.id,
            "productId": self.product_id,
            "events": self.events,
            "targetSalesAmount": self.target_sales_amount,
            "currency": self.currency,
            "recommendation": self.recommendation,
            "createdAt": self.created_at
        }
