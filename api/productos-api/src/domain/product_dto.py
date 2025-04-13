class ProductDTO:
    def __init__(self, id: str, name: str, description: str, price: float):
        self.id = id
        self.name = name
        self.description = description
        self.price = price

    def __repr__(self):
        return f"ProductDTO(id={self.id}, name={self.name}, description={self.description}, price={self.price})"