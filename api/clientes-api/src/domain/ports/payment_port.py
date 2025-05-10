from abc import ABC, abstractmethod


class PaymentPort(ABC):
    """Port defining the interface for payment processing"""

    @abstractmethod
    def process_payment(self, payment_info):
        """
        Process a payment with the given payment information.
        :param payment_info: Payment information to process.
        :return:
        """
        pass
