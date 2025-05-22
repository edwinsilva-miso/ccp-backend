import datetime

class ManufacturerDTO:
    def __init__(self, id: int, nit: str, name: str, address: str, phone: str, email: str, legal_representative: str,
                 country: str, status: str, created: datetime, updated: datetime):
        self.id = id
        self.nit = nit
        self.name = name
        self.address = address
        self.phone = phone
        self.email = email
        self.legal_representative = legal_representative
        self.country = country
        self.status = status
        self.created = created
        self.updated = updated

    def __str__(self):
        return f'{self.id} - {self.nit} - {self.name} - {self.address} - {self.phone} - {self.email} - {self.legal_representative} - {self.country} - {self.status} - {self.created} - {self.updated}'
