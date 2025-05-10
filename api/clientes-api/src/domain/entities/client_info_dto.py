class ClientInfoDTO:

    def __init__(self, name: str, address: str, phone: str, email: str, order_id: str):
        """
        Initialize a ClientDTO object with the given parameters.
        :param name: The name of the client.
        :param address: The address of the client.
        :param phone: The phone number of the client.
        :param email: The email address of the client.
        :param order_id: The unique identifier for the order associated with the client.
        """
        self.name = name
        self.address = address
        self.phone = phone
        self.email = email
        self.order_id = order_id

    def __str__(self):
        return f"ClientInfoDTO(name={self.name}, address={self.address}, phone={self.phone}, email={self.email})"

    def to_dict(self):
        """
        Convert the ClientInfoDTO object to a dictionary.
        :return: A dictionary representation of the ClientDTO object.
        """
        return {
            "name": self.name,
            "address": self.address,
            "phone": self.phone,
            "email": self.email
        }
