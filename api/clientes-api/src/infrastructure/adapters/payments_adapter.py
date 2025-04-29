import logging
import os

import requests

PAYMENT_GATEWAY_URL = os.getenv('PAYMENT_GATEWAY_URL')

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)
logger = logging.getLogger(__name__)


class PaymentsAdapter:

    def __init__(self):
        self.token = None

    def authenticate(self):
        """
        Obtain a JWT token from the payment gateway.
        :return: True if authentication is successful, False otherwise.
        """
        logging.info("Obtaining JWT token from payment gateway...")
        payload = {
            "client_id": os.getenv('CLIENT_ID'),
            "client_secret": os.getenv('CLIENT_SECRET'),
        }
        try:
            # Make a request to the payment gateway to validate the token
            response = requests.post(f"{PAYMENT_GATEWAY_URL}/auth/token/", json=payload)
            if response.status_code == 200:
                data = response.json()
                self.token = data['access_token']
                return True
            else:
                logging.warning(
                    f"Failed to authenticate with payment gateway: {response.status_code} - {response.text}")
                return response.json()
        except requests.RequestException as e:
            logging.error(f"Error connecting to payment gateway: {str(e)}")
            return False

    def get_headers(self):
        """
        Get the headers for the request to the payment gateway.
        :return: Dictionary of headers.
        """
        if not self.token:
            self.authenticate()
        return {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }

    def process_payment(self, payment_dto: dict):
        """
        Process a payment using the payment gateway.
        :param payment_dto: PaymentDTO object containing payment details.
        :return: Response from the payment gateway.
        """
        logging.debug("Processing payment...")
        headers = self.get_headers()

        try:
            response = requests.post(f"{PAYMENT_GATEWAY_URL}/payments/", json=payment_dto, headers=headers)
            if response.status_code == 201:
                return response.json()
            elif response.status_code == 402:
                print(f"Payment processing failed: {response.text}")
                return response.json()
            else:
                # Retry authentication if token is expired
                if response.status_code == 401 and "expired" in response.text.lower():
                    self.authenticate()
                    return self.process_payment(payment_dto)

                print(f"Payment processing failed: {response.text}")
                return None
        except requests.RequestException as e:
            logging.error(f"Error connecting to payment gateway: {str(e)}")
            return None
