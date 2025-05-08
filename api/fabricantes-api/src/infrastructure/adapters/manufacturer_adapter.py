from ..dao.manufacturer_dao import ManufacturerDAO
from ..mapper.manufacturer_mapper import ManufacturerMapper
from ...domain.entities.manufacturer_dto import ManufacturerDTO
from ...domain.repositories.manufacturer_repository import ManufacturerRepository


class ManufacturerAdapter(ManufacturerRepository):

    def get_all(self) -> list[ManufacturerDTO]:
        return ManufacturerMapper.to_dto_list(ManufacturerDAO.find_all())

    def get_by_id(self, id: str) -> ManufacturerDTO | None:
        manufacturer = ManufacturerDAO.find_by_id(id)
        return ManufacturerMapper.to_dto(manufacturer) if manufacturer else None

    def get_by_nit(self, nit: str) -> ManufacturerDTO | None:
        manufacturer = ManufacturerDAO.find_by_nit(nit)
        return ManufacturerMapper.to_dto(manufacturer) if manufacturer else None

    def get_by_email(self, email: str) -> ManufacturerDTO | None:
        manufacturer = ManufacturerDAO.find_by_email(email)
        return ManufacturerMapper.to_dto(manufacturer) if manufacturer else None

    def add(self, manufacturer: ManufacturerDTO) -> str:
        return ManufacturerDAO.save(ManufacturerMapper.to_domain(manufacturer))

    def update(self, manufacturer: ManufacturerDTO) -> ManufacturerDTO:
        updated_manufacturer = ManufacturerDAO.update(ManufacturerMapper.to_domain(manufacturer))
        return ManufacturerMapper.to_dto(updated_manufacturer)

    def delete(self, id: str) -> None:
        ManufacturerDAO.delete(id)
