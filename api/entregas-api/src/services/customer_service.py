from uuid import UUID

from ..models.models import Delivery

class CustomerService:
    """
    Service class for customer-related operations.
    """
    
    @staticmethod
    def get_customer_deliveries(customer_id: UUID):
        """
        Get all deliveries for a customer.
        
        Args:
            customer_id (int): The customer ID.
            
        Returns:
            list: The list of deliveries.
        """
        return Delivery.query.filter_by(customer_id=customer_id).all()
    
    @staticmethod
    def get_delivery(delivery_id, customer_id):
        """
        Get a specific delivery for a customer.
        
        Args:
            delivery_id (int): The delivery ID.
            customer_id (int): The customer ID.
            
        Returns:
            Delivery: The delivery if found and authorized, None otherwise.
        """
        delivery = Delivery.query.get(delivery_id)
        
        if not delivery or delivery.customer_id != customer_id:
            return None
        
        return delivery