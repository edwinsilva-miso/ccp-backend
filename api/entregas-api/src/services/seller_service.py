import logging
from ..models.models import db, Delivery, StatusUpdate


class SellerService:
    """
    Service class for seller-related operations.
    """

    @staticmethod
    def create_delivery(data):
        """
        Create a new delivery.
        
        Args:
            data (dict): The delivery data.
            
        Returns:
            Delivery: The created delivery.
        """
        logging.debug(f"creating new delivery for seller_id: {data['seller_id']}")
        # Create new delivery
        delivery = Delivery(
            customer_id=data['customer_id'],
            seller_id=data['seller_id'],
            description=data['description'],
            estimated_delivery_date=data.get('estimated_delivery_date')
        )

        # Add to database
        db.session.add(delivery)
        db.session.commit()

        # Create initial status update if provided
        if 'initial_status' in data:
            status_update = StatusUpdate(
                delivery_id=delivery.id,
                status=data['initial_status'],
                description=data.get('status_description', 'Delivery created')
            )
            db.session.add(status_update)
            db.session.commit()

        return delivery

    @staticmethod
    def get_seller_deliveries(seller_id):
        """
        Get all deliveries for a seller.
        
        Args:
            seller_id (int): The seller ID.
            
        Returns:
            list: The list of deliveries.
        """
        logging.debug(f"fetching all deliveries for seller_id: {seller_id}")
        return Delivery.query.filter_by(seller_id=seller_id).all()

    @staticmethod
    def get_delivery(delivery_id, seller_id):
        """
        Get a specific delivery for a seller.
        
        Args:
            delivery_id (int): The delivery ID.
            seller_id (int): The seller ID.
            
        Returns:
            Delivery: The delivery if found and authorized, None otherwise.
        """
        logging.debug(f"fetching delivery_id: {delivery_id} for seller_id: {seller_id}")
        delivery = Delivery.query.get(delivery_id)

        if not delivery or delivery.seller_id != seller_id:
            logging.debug(f"delivery not found or unauthorized access for delivery_id: {delivery_id}")
            return None

        return delivery

    @staticmethod
    def update_delivery(delivery_id, data):
        """
        Update a delivery.
        
        Args:
            delivery_id (int): The delivery ID.
            data (dict): The updated delivery data.
            
        Returns:
            Delivery: The updated delivery if found and authorized, None otherwise.
        """
        logging.debug(f"updating delivery_id: {delivery_id} for seller_id: {data['seller_id']}")
        delivery = Delivery.query.get(delivery_id)

        if not delivery or delivery.seller_id != data['seller_id']:
            logging.debug(f"delivery not found or unauthorized access for delivery_id: {delivery_id}")
            return None

        # Update fields
        if 'description' in data:
            delivery.description = data['description']
        if 'estimated_delivery_date' in data:
            delivery.estimated_delivery_date = data['estimated_delivery_date']

        db.session.commit()
        return delivery

    @staticmethod
    def delete_delivery(delivery_id, seller_id):
        """
        Delete a delivery.
        
        Args:
            delivery_id (int): The delivery ID.
            seller_id (int): The seller ID.
            
        Returns:
            bool: True if deleted successfully, False otherwise.
        """
        logging.debug(f"deleting delivery_id: {delivery_id} for seller_id: {seller_id}")
        delivery = Delivery.query.get(delivery_id)

        if not delivery or delivery.seller_id != seller_id:
            logging.debug(f"delivery not found or unauthorized access for delivery_id: {delivery_id}")
            return False

        db.session.delete(delivery)
        db.session.commit()
        return True

    @staticmethod
    def add_status_update(delivery_id, data):
        """
        Add a status update to a delivery.
        
        Args:
            delivery_id (int): The delivery ID.
            data (dict): The status update data.
            
        Returns:
            StatusUpdate: The created status update if authorized, None otherwise.
        """
        logging.debug(f"adding status update for delivery_id: {delivery_id}")
        delivery = Delivery.query.get(delivery_id)

        if not delivery or delivery.seller_id != data['seller_id']:
            logging.debug(f"delivery not found or unauthorized access for delivery_id: {delivery_id}")
            return None

        # Create status update
        status_update = StatusUpdate(
            delivery_id=delivery_id,
            status=data['status'],
            description=data.get('description')
        )

        db.session.add(status_update)
        db.session.commit()

        return status_update
