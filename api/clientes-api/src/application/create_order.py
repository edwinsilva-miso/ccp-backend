import logging
import uuid

from .utils.validation_utils import validate
from ..domain.entities.client_info_dto import ClientInfoDTO
from ..domain.entities.order_details_dto import OrderDetailsDTO
from ..domain.entities.order_dto import OrderDTO
from ..domain.entities.payment_dto import PaymentDTO

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)
logger = logging.getLogger(__name__)


class CreateOrder:
    """
    Use case for creating a purchase.
    """

    def __init__(self, order_repository, payments_port, messaging_port):
        self.order_repository = order_repository
        self.payments_port = payments_port
        self.messaging_port = messaging_port

    def execute(self, order_data):
        logging.debug("Starting purchase creation process...")
        # Validate the purchase data
        validate(order_data)

        # order = order_data['order']
        payment = order_data['payment']
        client_info = order_data['clientInfo']
        order_details = order_data['orderDetails']
        order_id = str(uuid.uuid4())

        # Create the order DTO
        order_dto = OrderDTO(
            id=order_id,
            client_id=order_data['clientId'],
            quantity=order_data['quantity'],
            subtotal=order_data['subtotal'],
            tax=order_data['tax'],
            total=order_data['total'],
            currency=order_data['currency'],
            status='PENDIENTE',
            created_at=None,
            updated_at=None
        )

        # Process the payment
        payment_dto = self._execute_payment(payment, order_id)

        order_dto.status = 'COMPLETADO' if payment_dto.status == 'APPROVED' else 'FALLIDO'
        order_dto.payment = payment_dto

        # Create the client info DTO
        client_info_dto = ClientInfoDTO(
            name=client_info['name'],
            address=client_info['address'],
            phone=client_info['phone'],
            email=client_info['email'],
            order_id=order_id
        )

        # Create the order details DTO
        list_order_details = [
            OrderDetailsDTO(
                id=str(uuid.uuid4()),
                order_id=order_id,
                product_id=item['productId'],
                quantity=item['quantity'],
                unit_price=item['unitPrice'],
                total_price=item['totalPrice'],
                currency=item['currency']
            ) for item in order_details
        ]

        # Set the order information in the DTO
        order_dto.order_details = list_order_details
        order_dto.client_info = client_info_dto

        # Create the purchase
        logging.debug(f"Purchase data: {order_dto.to_dict()}")
        purchase = self.order_repository.add(order_dto)
        logging.debug(f"Purchase created with ID: {purchase.id} and status: {purchase.status}")

        order_message = purchase.to_dict()
        # Send messages
        if purchase.status == 'COMPLETADO':
            self._update_products_stock(purchase.order_details)
            self._produce_order(order_message)

        # Create the DTO to send to pedidos-api

        logging.debug(f"Order created with detail: {order_message}")
        operation_status = 402 if purchase.status == 'FALLIDO' else 201
        return order_message, operation_status

    def _execute_payment(self, payment_info, order_id):
        """
        Process the payment using the payment port.
        :param payment_info: The payment information to process.
        :return: The response from the payment processing.
        """
        logging.debug("Processing payment...")
        payload = {
            "amount": payment_info['amount'],
            "cardNumber": payment_info['cardNumber'],
            "cvv": payment_info['cvv'],
            "expiryDate": payment_info['expiryDate'],
            "currency": payment_info['currency'],
        }
        result = self.payments_port.process_payment(payload)
        if result is None:
            logger.error("Payment processing failed.")
            return None

        logger.info(
            f'Payment executed with transaction ID {result["transactionReference"]} and result: {result["status"]}')

        # Update the payment DTO with the response
        payment_dto = PaymentDTO(
            id=result['id'],
            order_id=order_id,
            amount=payment_info['amount'],
            card_number=result['cardNumber'],
            cvv=payment_info['cvv'],
            expiry_date=payment_info['expiryDate'],
            currency=payment_info['currency']
        )
        payment_dto.transaction_id = result['transactionReference']
        payment_dto.status = result['status']
        payment_dto.transaction_date = result['timestamp']

        return payment_dto

    def _update_products_stock(self, order_details: list[OrderDetailsDTO]):
        """
        Update the stock of products after a successful purchase.
        :param order_details: List of order details containing product IDs and quantities.
        """
        logging.debug("Updating product stock...")
        products_dict = list[dict]()
        for item in order_details:
            detail = {
                "productId": item.product_id,
                "quantity": int(item.quantity)
            }
            products_dict.append(detail)

        message = {
            "products": products_dict,
        }
        logging.debug(f"Stock update message: {message}")
        self.messaging_port.send_message(
            exchange="update_stock_exchange",
            routing_key="update_stock_routing_key",
            message=message
        )
        logging.debug("Product stock update message sent.")

    def _produce_order(self, order_info: dict):
        """
        Produce the order to the messaging system.
        :param order_info: The order info produce.
        """
        logging.debug("Producing order to messaging system...")
        payment_data = order_info.get('payment')
        order_details_data = order_info.get('orderDetails', [])

        order_items = list()
        for detail in order_details_data:
            item = {
                "id": detail.get('id'),
                "productId": detail.get('product_id'),
                "quantity": detail.get('quantity'),
                "unitPrice": detail.get('unit_price'),
                "totalPrice": detail.get('total_price'),
                "currency": detail.get('currency')
            }
            order_items.append(item)

        order_data = {
            "id": order_info.get('id'),
            "orderDate": order_info.get('createdAt'),
            "status": 'INICIADO',
            "subtotal": order_info.get('subtotal'),
            "taxes": order_info.get('tax'),
            "total": order_info.get('total'),
            "currency": order_info.get('currency'),
            "clientId": order_info.get('clientId'),
            "paymentId": payment_data.get('id'),
            "transactionStatus": payment_data.get('status'),
            "transactionDate": payment_data.get('transactionDate'),
            "transactionId": payment_data.get('transactionId'),
            "items": order_items
        }

        message = {
            "order": order_data
        }

        logging.debug(f"Producing order {message}")

        self.messaging_port.send_message(
            exchange="order_initiated_exchange",
            routing_key="order_initiated_routing_key",
            message=message
        )
        logging.debug("Order produced to messaging system.")
