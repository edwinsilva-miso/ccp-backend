from ..dao.provider_dao import ProviderDAO
from ..mapper.provider_mapper import ProviderMapper
from ...domain.entities.provider_dto import ProviderDTO
from ...domain.repositories.provider_repository import ProviderRepository


class ProviderAdapter(ProviderRepository):

    def get_all(self) -> list[ProviderDTO]:
        return ProviderMapper.to_dto_list(ProviderDAO.find_all())

    def get_by_id(self, id: str) -> ProviderDTO | None:
        provider = ProviderDAO.find_by_id(id)
        return ProviderMapper.to_dto(provider) if provider else None

    def get_by_nit(self, nit: str) -> ProviderDTO | None:
        provider = ProviderDAO.find_by_nit(nit)
        return ProviderMapper.to_dto(provider) if provider else None

    def add(self, provider: ProviderDTO) -> str:
        return ProviderDAO.save(ProviderMapper.to_domain(provider))

    def update(self, provider: ProviderDTO) -> ProviderDTO:
        updated_provider = ProviderDAO.update(ProviderMapper.to_domain(provider))
        return ProviderMapper.to_dto(updated_provider)

    def delete(self, id: str) -> None:
        ProviderDAO.delete(id)
