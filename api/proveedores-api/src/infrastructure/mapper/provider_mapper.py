import datetime

from ...domain.entities.provider_dto import ProviderDTO
from ..model.provider_model import ProviderModel

class ProviderMapper:

    @staticmethod
    def to_domain(provider_dto: ProviderDTO) -> ProviderModel | None:
        """
        Converts a ProviderDTO to a ProviderModel.
        :param provider_dto:
        :return:
        """
        if provider_dto is None:
            return None

        created_at = datetime.datetime.fromisoformat(provider_dto.created) if isinstance(provider_dto.created,
                                                                                          str) else provider_dto.created
        updated_at = datetime.datetime.fromisoformat(provider_dto.updated) if isinstance(provider_dto.updated,
                                                                                          str) else provider_dto.updated

        return ProviderModel(
            id=provider_dto.id,
            nit=provider_dto.nit,
            name=provider_dto.name,
            address=provider_dto.address,
            phone=provider_dto.phone,
            email=provider_dto.email,
            legal_representative=provider_dto.legal_representative,
            country=provider_dto.country,
            status=provider_dto.status,
            createdAt=created_at,
            updatedAt=updated_at
        )

    @staticmethod
    def to_dto(provider: ProviderModel) -> ProviderDTO | None:
        """
        Converts a ProviderModel to a ProviderDTO.
        :param provider:
        :return:
        """
        if provider is None:
            return None

        created_at = provider.createdAt.isoformat() if provider.createdAt else None
        updated_at = provider.updatedAt.isoformat() if provider.updatedAt else None

        return ProviderDTO(
            provider.id,
            provider.nit,
            provider.name,
            provider.address,
            provider.phone,
            provider.email,
            provider.legal_representative,
            provider.country,
            provider.status if isinstance(provider.status, str) else provider.status.value,
            created_at,
            updated_at
        )

    @staticmethod
    def to_domain_list(providers_dto: list[ProviderDTO]) -> list[ProviderModel]:
        """
        Converts a list of ProviderDTO to a list of ProviderModel.
        :param providers_dto:
        :return:
        """
        return [ProviderMapper.to_domain(provider_dto) for provider_dto in providers_dto]

    @staticmethod
    def to_dto_list(providers: list[ProviderModel]) -> list[ProviderDTO]:
        """
        Converts a list of ProviderModel to a list of ProviderDTO.
        :param providers:
        :return:
        """
        return [ProviderMapper.to_dto(provider) for provider in providers]