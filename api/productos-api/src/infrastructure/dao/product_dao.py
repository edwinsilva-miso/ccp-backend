from datetime import datetime, timezone

from ..database.declarative_base import Session
from ..model.product_model import ProductModel


class ProductDAO:
    """
    Data Access Object for product.
    """

    @classmethod
    def save(cls, product: ProductModel) -> str:
        """
        Save a product to the database.
        :param product: ProductModel to save.
        :return: ID of the saved product.
        """
        session = Session()
        session.add(product)
        session.commit()
        session.refresh(product)
        session.close()
        return product.id

    @classmethod
    def find_all(cls) -> list[ProductModel]:
        """
        Obtain a list of products registered in the database
        :return: List of products
        """
        session = Session()
        products = session.query(ProductModel).all()
        session.close()
        return products

    @classmethod
    def find_by_id(cls, product_id: str) -> ProductModel | None:
        """
        Find a product by ID.
        :param product_id: ID of the product to find.
        :return: ProductModel if found, None otherwise.
        """
        session = Session()
        product = session.query(ProductModel).filter(ProductModel.id == product_id).first()
        session.close()
        return product

    @classmethod
    def find_by_name(cls, name: str) -> ProductModel | None:
        """
        Find a product by name.
        :param name: Name of the product to find.
        :return: ProductModel if found, None otherwise.
        """
        session = Session()
        product = session.query(ProductModel).filter(ProductModel.name == name).first()
        session.close()
        return product

    @classmethod
    def find_by_manufacturer(cls, manufacturer_id: str) -> list[ProductModel]:
        """
        Find products by manufacturer ID.
        :param manufacturer_id: ID of the manufacturer to find products for.
        :return: List of ProductModel if found, empty list otherwise.
        """
        session = Session()
        products = session.query(ProductModel).filter(ProductModel.manufacturer_id == manufacturer_id).all()
        session.close()
        return products

    @classmethod
    def update(cls, product: ProductModel) -> ProductModel | None:
        """
        Update a product in the database.
        :param product: ProductModel to update.
        :return: Updated ProductModel.
        """
        session = Session()
        try:
            existing_product = session.query(ProductModel).filter(ProductModel.id == product.id).first()
            if existing_product:
                # Update fields
                existing_product.name = product.name
                existing_product.brand = product.brand
                existing_product.manufacturer_id = product.manufacturer_id
                existing_product.description = product.description
                existing_product.stock = product.stock
                existing_product.details = product.details
                existing_product.storage_conditions = product.storage_conditions
                existing_product.price = product.price
                existing_product.currency = product.currency
                existing_product.delivery_time = product.delivery_time
                existing_product.images = product.images
                existing_product.updatedAt = datetime.now(timezone.utc)

                # Commit the changes
                session.commit()

                # Create a copy of the data to return (detached from session)
                result = ProductModel(
                    id=existing_product.id,
                    name=existing_product.name,
                    brand=existing_product.brand,
                    description=existing_product.description,
                    stock=existing_product.stock,
                    details=existing_product.details,
                    storage_conditions=existing_product.storage_conditions,
                    price=existing_product.price,
                    currency=existing_product.currency,
                    delivery_time=existing_product.delivery_time,
                    manufacturer_id=existing_product.manufacturer_id,
                    images=existing_product.images,
                    createdAt=existing_product.createdAt,
                    updatedAt=existing_product.updatedAt
                )

                return result
            return None
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @classmethod
    def delete(cls, product_id: str) -> bool:
        """
        Delete a product from the database.
        :param product_id: ID of the product to delete.
        :return: True if deleted, False otherwise.
        """
        session = Session()
        session.query(ProductModel).filter(ProductModel.id == product_id).delete()
        session.commit()
        session.close()
