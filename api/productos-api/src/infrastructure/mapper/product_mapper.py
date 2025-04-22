import datetime
import json

from ..model.product_model import ProductModel
from ...domain.entities.product_dto import ProductDTO


class ProductMapper:

    @staticmethod
    def to_domain(product_dto: ProductDTO) -> ProductModel | None:
        """
        Converts a ProductDTO to a ProductModel.
        :param product_dto:
        :return:
        """
        if product_dto is None:
            return None

        created = datetime.datetime.fromisoformat(product_dto.created_at) if isinstance(product_dto.created_at,
                                                                                        str) else product_dto.created_at
        updated = datetime.datetime.fromisoformat(product_dto.updated_at) if isinstance(product_dto.updated_at,
                                                                                        str) else product_dto.updated_at
        # Convert details from dict to JSON string
        details_json = json.dumps(product_dto.details) if product_dto.details else None

        return ProductModel(
            id=product_dto.id,
            name=product_dto.name,
            brand=product_dto.brand,
            description=product_dto.description,
            stock=product_dto.stock,
            details=details_json,
            storage_conditions=product_dto.storage_conditions,
            price=product_dto.price,
            currency=product_dto.currency,
            delivery_time=product_dto.delivery_time,
            images=product_dto.images,
            manufacturer_id=product_dto.manufacturer_id,
            createdAt=created,
            updatedAt=updated
        )

    @staticmethod
    def to_dto(product: ProductModel) -> ProductDTO | None:
        """
        Converts a ProductModel to a ProductDTO.
        :param product:
        :return:
        """
        if product is None:
            return None

        created_at = product.createdAt.isoformat() if product.createdAt else None
        updated_at = product.updatedAt.isoformat() if product.updatedAt else None

        # Parse JSON string back to dict
        details_dict = json.loads(product.details) if product.details else None

        return ProductDTO(
            id=product.id,
            manufacturer_id=product.manufacturer_id,
            name=product.name,
            brand=product.brand,
            description=product.description,
            stock=product.stock,
            details=details_dict,
            storage_conditions=product.storage_conditions,
            price=product.price,
            currency=product.currency,
            delivery_time=product.delivery_time,
            images=product.images,
            created_at=created_at,
            updated_at=updated_at
        )

    @staticmethod
    def to_dto_list(products: list[ProductModel]) -> list[ProductDTO]:
        """
        Converts a list of ProductModel to a list of ProductDTO.
        :param products:
        :return:
        """
        return [ProductMapper.to_dto(product) for product in products]

    @staticmethod
    def to_domain_list(products_dto: list[ProductDTO]) -> list[ProductModel]:
        """
        Converts a list of ProductDTO to a list of ProductModel.
        :param products_dto:
        :return:
        """
        return [ProductMapper.to_domain(product_dto) for product_dto in products_dto]
