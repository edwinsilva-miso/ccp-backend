class SellingPlanDTO:
    """
    Data Transfer Object for Selling Plan.
    """

    def __init__(self, id: str, user_id: str, title: str, description: str, target_amount: float = None,
                 target_date: str = None, status: str = "active", created_at: str = None):
        """
        Initialize a new SellingPlanDTO.
        
        :param id: Unique identifier for the selling plan
        :param user_id: ID of the user (seller) who owns this plan
        :param title: Title of the selling plan
        :param description: Detailed description of the selling plan
        :param target_amount: Optional target amount for the selling plan
        :param target_date: Optional target date for the selling plan
        :param status: Status of the selling plan (active, completed, cancelled)
        :param created_at: Creation timestamp
        """
        self.id = id
        self.user_id = user_id
        self.title = title
        self.description = description
        self.target_amount = target_amount
        self.target_date = target_date
        self.status = status
        self.created_at = created_at

    def __repr__(self):
        return f"SellingPlanDTO(id={self.id}, user_id={self.user_id}, title={self.title}, " \
               f"description={self.description}, target_amount={self.target_amount}, " \
               f"target_date={self.target_date}, status={self.status}, created_at={self.created_at})"

    def to_dict(self):
        """
        Convert the DTO to a dictionary.
        :return: Dictionary representation of the DTO.
        """
        return {
            "id": self.id,
            "userId": self.user_id,
            "title": self.title,
            "description": self.description,
            "targetAmount": self.target_amount,
            "targetDate": self.target_date,
            "status": self.status,
            "createdAt": self.created_at
        }