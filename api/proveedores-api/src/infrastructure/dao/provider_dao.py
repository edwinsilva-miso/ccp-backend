import datetime
from datetime import datetime

from ..database.declarative_base import Session
from ..model.provider_model import ProviderModel


class ProviderDAO:
    """
    Data Access Object for Provider.
    """

    @classmethod
    def save(cls, provider: ProviderModel) -> str:
        """
        Save a provider to the database.
        :param provider: ProviderModel to save.
        :return: ID of the saved provider.
        """
        session = Session()
        session.add(provider)
        session.commit()
        session.refresh(provider)
        session.close()
        return provider.id

    @classmethod
    def find_all(cls) -> list[ProviderModel]:
        """
        Obtain a list of providers registered in the database
        :return: List of providers
        """
        session = Session()
        providers = session.query(ProviderModel).all()
        session.close()
        return providers

    @classmethod
    def find_by_id(cls, provider_id: str) -> ProviderModel | None:
        """
        Find a provider by ID.
        :param provider_id: ID of the provider to find.
        :return: ProviderModel if found, None otherwise.
        """
        session = Session()
        provider = session.query(ProviderModel).filter(ProviderModel.id == provider_id).first()
        session.close()
        return provider

    @classmethod
    def find_by_nit(cls, nit: str) -> ProviderModel | None:
        """
        Find a provider by ID.
        :param nit: Identification of the provider to find.
        :return: ProviderModel if found, None otherwise.
        """
        session = Session()
        provider = session.query(ProviderModel).filter(ProviderModel.nit == nit).first()
        session.close()
        return provider

    @classmethod
    def update(cls, provider: ProviderModel) -> ProviderModel:
        """
        Update the data for an existing provider
        :param provider: A provider with updated data
        :return: updated provider
        """
        session = Session()
        existing = session.query(ProviderModel).filter(ProviderModel.id == provider.id).first()
        if existing:
            existing.name = provider.name
            existing.address = provider.address
            existing.phone = provider.phone
            existing.email = provider.email
            existing.legal_representative = provider.legal_representative
            existing.country = provider.country
            existing.status = provider.status
            existing.updatedAt = datetime.now(datetime.UTC)
            session.merge(existing)
            session.commit()
        session.close()
        return provider

    @classmethod
    def delete(self, provider_id: str) -> None:
        """
        Delete permanently a provider
        :param provider_id: ID of the provider to delete
        :return:
        """
        session = Session()
        session.query(ProviderModel).filter(ProviderModel.id == provider_id).delete()
        session.commit()
        session.close()
