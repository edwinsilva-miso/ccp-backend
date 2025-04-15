import datetime

from ...domain.entities.manufacturer_dto import ManufacturerDTO
from ..model.manufacturer_model import ManufacturerModel

class ManufacturerMapper:

    @staticmethod
    def to_domain(manufacturer_dto: ManufacturerDTO) -> ManufacturerModel | None:
        """
        Converts a ManufacturerDTO to a ManufacturerModel.
        :param manufacturer_dto:
        :return:
        """
        if manufacturer_dto is None:
            return None

        created_at = datetime.datetime.fromisoformat(manufacturer_dto.created) if isinstance(manufacturer_dto.created,
                                                                                          str) else manufacturer_dto.created
        updated_at = datetime.datetime.fromisoformat(manufacturer_dto.updated) if isinstance(manufacturer_dto.updated,
                                                                                          str) else manufacturer_dto.updated

        return ManufacturerModel(
            id=manufacturer_dto.id,
            nit=manufacturer_dto.nit,
            name=manufacturer_dto.name,
            address=manufacturer_dto.address,
            phone=manufacturer_dto.phone,
            email=manufacturer_dto.email,
            legal_representative=manufacturer_dto.legal_representative,
            country=manufacturer_dto.country,
            status=manufacturer_dto.status,
            createdAt=created_at,
            updatedAt=updated_at
        )

    @staticmethod
    def to_dto(manufacturer: ManufacturerModel) -> ManufacturerDTO | None:
        """
        Converts a ManufacturerModel to a ManufacturerDTO.
        :param manufacturer:
        :return:
        """
        if manufacturer is None:
            return None

        created_at = manufacturer.createdAt.isoformat() if manufacturer.createdAt else None
        updated_at = manufacturer.updatedAt.isoformat() if manufacturer.updatedAt else None

        return ManufacturerDTO(
            manufacturer.id,
            manufacturer.nit,
            manufacturer.name,
            manufacturer.address,
            manufacturer.phone,
            manufacturer.email,
            manufacturer.legal_representative,
            manufacturer.country,
            manufacturer.status if isinstance(manufacturer.status, str) else manufacturer.status.value,
            created_at,
            updated_at
        )

    @staticmethod
    def to_domain_list(manufacturers_dto: list[ManufacturerDTO]) -> list[ManufacturerModel]:
        """
        Converts a list of ManufacturerDTO to a list of ManufacturerModel.
        :param manufacturers_dto:
        :return:
        """
        return [ManufacturerMapper.to_domain(manufacturer_dto) for manufacturer_dto in manufacturers_dto]

    @staticmethod
    def to_dto_list(manufacturers: list[ManufacturerModel]) -> list[ManufacturerDTO]:
        """
        Converts a list of ManufacturerModel to a list of ManufacturerDTO.
        :param manufacturers:
        :return:
        """
        return [ManufacturerMapper.to_dto(manufacturer) for manufacturer in manufacturers]