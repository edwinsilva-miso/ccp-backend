import logging
from uuid import UUID
from ..models.models import db, Delivery, StatusUpdate


class SellerService:
    """
    Service class for seller-related operations.
    """

    @staticmethod
    def create_delivery(data: dict):
        """
        Create a new delivery.

        Args:
            data (dict): The delivery data.

        Returns:
            Delivery: The created delivery.
        """

        try:
            # Convert string IDs to UUID if they are strings
            customer_id = UUID(data['customer_id']) if isinstance(data['customer_id'], str) else data['customer_id']
            seller_id = UUID(data['seller_id']) if isinstance(data['seller_id'], str) else data['seller_id']
            order_id = UUID(data['order_id']) if isinstance(data.get('order_id'), str) else data.get('order_id')

            logging.debug(f"creating new delivery for seller_id: {seller_id}")
            # Create new delivery
            delivery = Delivery(
                customer_id=customer_id,
                seller_id=seller_id,
                description=data['description'],
                estimated_delivery_date=data.get('estimated_delivery_date'),
                order_id=order_id
            )
        except Exception as e:
            logging.error(f"Invalid UUID format: {str(e)}")
            raise Exception(f"Invalid UUID format: {str(e)}")

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
    def get_seller_deliveries(seller_id: UUID):
        """
        Get all deliveries for a seller.

        Args:
            seller_id (UUID): The seller ID.

        Returns:
            list: The list of deliveries.
        """
        logging.debug(f"fetching all deliveries for seller_id: {seller_id}")
        return Delivery.query.filter_by(seller_id=seller_id).all()

    @staticmethod
    def get_delivery(delivery_id: UUID, seller_id: UUID):
        """
        Get a specific delivery for a seller.

        Args:
            delivery_id (UUID): The delivery ID.
            seller_id (UUID): The seller ID.

        Returns:
            Delivery: The delivery if found and authorized, None otherwise.
        """
        logging.debug(f"fetching delivery_id: {delivery_id} for seller_id: {seller_id}")
        delivery = Delivery.query.get(delivery_id)

        if not delivery:
            logging.debug(f"delivery not found: {delivery_id}")
            return None
        if str(delivery.seller_id) != seller_id:
            logging.debug(f"unauthorized access for delivery_id: {delivery_id}")
            return None

        return delivery

    @staticmethod
    def get_delivery_by_order_id(order_id: UUID, seller_id: UUID):
        """
        Get a specific delivery for a seller by order_id.

        Args:
            order_id (UUID): The order ID.
            seller_id (UUID): The seller ID.

        Returns:
            Delivery: The delivery if found and authorized, None otherwise.
        """
        logging.debug(f"fetching delivery with order_id: {order_id} for seller_id: {seller_id}")
        delivery = Delivery.query.filter_by(order_id=order_id, seller_id=seller_id).first()

        if not delivery:
            logging.debug(f"delivery not found for order_id: {order_id}")
            return None

        return delivery

    @staticmethod
    def update_delivery(delivery_id: UUID, data: dict):
        """
        Update a delivery.

        Args:
            delivery_id (UUID): The delivery ID.
            data (dict): The updated delivery data.

        Returns:
            Delivery: The updated delivery if found and authorized, None otherwise.
        """
        logging.debug(f"updating delivery_id: {delivery_id} for seller_id: {data['seller_id']}")
        delivery = Delivery.query.get(delivery_id)

        logging.debug(f"found delivery object: {delivery is not None}")

        if not delivery:
            logging.debug(f"delivery not found: {delivery_id}")
            return None
        if str(delivery.seller_id) != data['seller_id']:
            logging.debug(f"unauthorized access for delivery_id: {delivery_id}")
            return None

        # Update fields
        if 'description' in data:
            logging.debug(f"updating description from '{delivery.description}' to '{data['description']}'")
            delivery.description = data['description']
        if 'estimated_delivery_date' in data:
            logging.debug(
                f"updating estimated_delivery_date from '{delivery.estimated_delivery_date}' to '{data['estimated_delivery_date']}'")
            delivery.estimated_delivery_date = data['estimated_delivery_date']
        if 'order_id' in data:
            logging.debug(f"updating order_id from '{delivery.order_id}' to '{data['order_id']}'")
            delivery.order_id = data['order_id']

        db.session.commit()
        logging.debug(f"successfully updated delivery {delivery_id}")
        return delivery

    @staticmethod
    def delete_delivery(delivery_id: UUID, seller_id: UUID):
        """
        Delete a delivery.

        Args:
            delivery_id (UUID): The delivery ID.
            seller_id (UUID): The seller ID.

        Returns:
            bool: True if deleted successfully, False otherwise.
        """
        logging.debug(f"deleting delivery_id: {delivery_id} for seller_id: {seller_id}")
        delivery = Delivery.query.get(delivery_id)

        if not delivery:
            logging.debug(f"delivery not found: {delivery_id}")
            return None
        if str(delivery.seller_id) != seller_id:
            logging.debug(f"unauthorized access for delivery_id: {delivery_id}")
            return None

        db.session.delete(delivery)
        db.session.commit()
        return True

    @staticmethod
    def add_status_update(delivery_id: UUID, data: dict):
        """
        Add a status update to a delivery.

        Args:
            delivery_id (UUID): The delivery ID.
            data (dict): The status update data.

        Returns:
            StatusUpdate: The created status update if authorized, None otherwise.
        """
        logging.debug(f"adding status update for delivery_id: {delivery_id}")
        delivery = Delivery.query.get(delivery_id)

        if not delivery or str(delivery.seller_id) != data['seller_id']:
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

    @staticmethod
    def update_status_update(status_update_id: UUID, data: dict):
        """
        Update a status update.

        Args:
            status_update_id (UUID): The status update ID.
            data (dict): The updated status update data.

        Returns:
            StatusUpdate: The updated status update if authorized, None otherwise.
        """
        logging.debug(f"updating status_update_id: {status_update_id}")
        status_update = StatusUpdate.query.get(status_update_id)

        if not status_update:
            logging.debug(f"status update not found: {status_update_id}")
            return None

        # Get the delivery to check seller authorization
        delivery = Delivery.query.get(status_update.delivery_id)

        if not delivery or str(delivery.seller_id) != data['seller_id']:
            logging.debug(f"unauthorized access for status_update_id: {status_update_id}")
            return None

        # Update fields
        if 'status' in data:
            logging.debug(f"updating status from '{status_update.status}' to '{data['status']}'")
            status_update.status = data['status']
        if 'description' in data:
            logging.debug(f"updating description from '{status_update.description}' to '{data['description']}'")
            status_update.description = data['description']
        if 'created_at' in data:
            logging.debug(f"updating created_at from '{status_update.created_at}' to '{data['created_at']}'")
            status_update.created_at = data['created_at']

        db.session.commit()
        logging.debug(f"successfully updated status update {status_update_id}")
        return status_update

    @staticmethod
    def delete_status_update(status_update_id: UUID, seller_id: UUID):
        """
        Delete a status update.

        Args:
            status_update_id (UUID): The status update ID.
            seller_id (UUID): The seller ID.

        Returns:
            bool: True if deleted successfully, None otherwise.
        """
        logging.debug(f"deleting status_update_id: {status_update_id}")
        status_update = StatusUpdate.query.get(status_update_id)

        if not status_update:
            logging.debug(f"status update not found: {status_update_id}")
            return None

        # Get the delivery to check seller authorization
        delivery = Delivery.query.get(status_update.delivery_id)

        if not delivery or str(delivery.seller_id) != seller_id:
            logging.debug(f"unauthorized access for status_update_id: {status_update_id}")
            return None

        db.session.delete(status_update)
        db.session.commit()
        return True
