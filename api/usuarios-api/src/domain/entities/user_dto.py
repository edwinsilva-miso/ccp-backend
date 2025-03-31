class UserDTO:
    def __init__(self, id: str, name: str, phone: str, email: str, password: str, salt: str, role: str):
        self.id = id
        self.name = name
        self.phone = phone
        self.email = email
        self.password = password
        self.salt = salt
        self.role = role

    def __str__(self):
        return f'{self.id} - {self.name} - {self.phone} - {self.email} - {self.role}'
