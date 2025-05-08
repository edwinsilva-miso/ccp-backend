from datetime import datetime, timezone


from ..database.declarative_base import Session
from ..model.manufacturer_model import ManufacturerModel


class ManufacturerDAO:
    """
    Data Access Object for manufacturer.
    """

    @classmethod
    def save(cls, manufacturer: ManufacturerModel) -> str:
        """
        Save a manufacturer to the database.
        :param manufacturer: ManufacturerModel to save.
        :return: ID of the saved manufacturer.
        """
        session = Session()
        session.add(manufacturer)
        session.commit()
        session.refresh(manufacturer)
        session.close()
        return manufacturer.id

    @classmethod
    def find_all(cls) -> list[ManufacturerModel]:
        """
        Obtain a list of manufacturers registered in the database
        :return: List of manufacturers
        """
        session = Session()
        manufacturers = session.query(ManufacturerModel).all()
        session.close()
        return manufacturers

    @classmethod
    def find_by_id(cls, manufacturer_id: str) -> ManufacturerModel | None:
        """
        Find a manufacturer by ID.
        :param manufacturer_id: ID of the manufacturer to find.
        :return: ManufacturerModel if found, None otherwise.
        """
        session = Session()
        manufacturer = session.query(ManufacturerModel).filter(ManufacturerModel.id == manufacturer_id).first()
        session.close()
        return manufacturer

    @classmethod
    def find_by_nit(cls, nit: str) -> ManufacturerModel | None:
        """
        Find a manufacturer by ID.
        :param nit: Identification of the manufacturer to find.
        :return: ManufacturerModel if found, None otherwise.
        """
        session = Session()
        manufacturer = session.query(ManufacturerModel).filter(ManufacturerModel.nit == nit).first()
        session.close()
        return manufacturer

    @classmethod
    def find_by_email(cls, email: str) -> ManufacturerModel | None:
        """
        Find a manufacturer by EMAIL.
        :param email: Email of the manufacturer to find.
        :return: ManufacturerModel if found, None otherwise.
        """
        session = Session()
        manufacturer = session.query(ManufacturerModel).filter(ManufacturerModel.email == email).first()
        session.close()
        return manufacturer

    @classmethod
    def update(cls, manufacturer: ManufacturerModel) -> ManufacturerModel | None:
        """
        Update the data for an existing manufacturer
        :param manufacturer: A manufacturer with updated data
        :return: updated manufacturer
        """
        session = Session()
        try:
            # Since the use case already validated existence, we can directly query
            existing = session.query(ManufacturerModel).with_for_update().filter(
                ManufacturerModel.id == manufacturer.id
            ).first()

            if existing:
                # Update fields

                existing.name = manufacturer.name
                existing.address = manufacturer.address
                existing.phone = manufacturer.phone
                existing.email = manufacturer.email
                existing.legal_representative = manufacturer.legal_representative
                existing.country = manufacturer.country
                existing.status = manufacturer.status
                existing.updatedAt = datetime.now(timezone.utc)

                # Commit changes
                session.commit()

                # Create a copy of the data to return (detached from session)
                result = ManufacturerModel(
                    id=existing.id,
                    name=existing.name,
                    address=existing.address,
                    phone=existing.phone,
                    email=existing.email,
                    legal_representative=existing.legal_representative,
                    country=existing.country,
                    status=existing.status,
                    nit=existing.nit,
                    createdAt=existing.createdAt,
                    updatedAt=existing.updatedAt
                )
                return result
            return None
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @classmethod
    def delete(self, manufacturer_id: str) -> None:
        """
        Delete permanently a manufacturer
        :param manufacturer_id: ID of the manufacturer to delete
        :return:
        """
        session = Session()
        session.query(ManufacturerModel).filter(ManufacturerModel.id == manufacturer_id).delete()
        session.commit()
        session.close()
