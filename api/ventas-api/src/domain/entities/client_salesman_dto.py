class ClientSalesmanDTO:
    """
    Data Transfer Object for Client Salesman.
    """

    def __init__(self, id: str, salesman_id: str, client_id: str, client_name: str, client_phone: str,
                 client_email: str,
                 address: str, city: str, country: str, store_name: str):
        self.id = id
        self.salesman_id = salesman_id
        self.client_id = client_id
        self.client_name = client_name
        self.client_phone = client_phone
        self.client_email = client_email
        self.address = address
        self.city = city
        self.country = country
        self.store_name = store_name

    def __repr__(self):
        return f"ClientSalesmanDTO(id={self.id}, salesman_id={self.salesman_id}, client_id={self.client_id}, " \
               f"client_name={self.client_name}, client_phone={self.client_phone}, client_email={self.client_email}, " \
               f"address={self.address}, city={self.city}, country={self.country}, store_name={self.store_name})"

    def to_dict(self):
        """
        Convert the DTO to a dictionary.
        :return: Dictionary representation of the DTO.
        """
        return {
            "id": self.id,
            "salesmanId": self.salesman_id,
            "clientId": self.client_id,
            "clientName": self.client_name,
            "clientPhone": self.client_phone,
            "clientEmail": self.client_email,
            "address": self.address,
            "city": self.city,
            "country": self.country,
            "storeName": self.store_name
        }
