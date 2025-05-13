import logging
from ..model.warehouse_model import WarehouseModel
from ...domain.entities.warehouse_dto import WarehouseDTO

logger = logging.getLogger(__name__)


class WarehouseMapper:
    """
    Mapper class to convert between WarehouseDTO and WarehouseModel.
    """

    @staticmethod
    def to_dto(model: WarehouseModel) -> WarehouseDTO:
        """
        Convert a WarehouseModel to a WarehouseDTO.
        :param model: WarehouseModel to convert.
        :return: Converted WarehouseDTO.
        """
        logger.debug(f"converting warehouse model to dto: {model.__dict__}")
        dto = WarehouseDTO(
            id=str(model.id),
            location=model.location,
            description=model.description,
            name=model.name,
            administrator_id=str(model.administrator_id),
            status=model.status,
            created_at=model.created_at.isoformat() if model.created_at else None,
            updated_at=model.updated_at.isoformat() if model.updated_at else None
        )
        logger.debug(f"successfully converted to dto: {dto.__dict__}")
        return dto

    @staticmethod
    def to_model(dto: WarehouseDTO) -> WarehouseModel:
        """
        Convert a WarehouseDTO to a WarehouseModel.
        :param dto: WarehouseDTO to convert.
        :return: Converted WarehouseModel.
        """
        logger.debug(f"converting warehouse dto to model: {dto.__dict__}")
        model = WarehouseModel(
            id=dto.id,
            location=dto.location,
            description=dto.description,
            name=dto.name,
            administrator_id=dto.administrator_id,
            status=dto.status
        )
        logger.debug(f"successfully converted to model: {model.__dict__}")
        return model

    @staticmethod
    def to_dto_list(models: list[WarehouseModel]) -> list[WarehouseDTO]:
        """
        Convert a list of WarehouseModel to a list of WarehouseDTO.
        :param models: List of WarehouseModel to convert.
        :return: List of converted WarehouseDTO.
        """
        logger.debug(f"converting list of {len(models)} warehouse models to dtos")
        dtos = [WarehouseMapper.to_dto(model) for model in models]
        logger.debug(f"successfully converted {len(dtos)} models to dtos")
        return dtos

    @staticmethod
    def to_model_list(dtos: list[WarehouseDTO]) -> list[WarehouseModel]:
        """
        Convert a list of WarehouseDTO to a list of WarehouseModel.
        :param dtos: List of WarehouseDTO to convert.
        :return: List of converted WarehouseModel.
        """
        logger.debug(f"converting list of {len(dtos)} warehouse dtos to models")
        models = [WarehouseMapper.to_model(dto) for dto in dtos]
        logger.debug(f"successfully converted {len(models)} dtos to models")
        return models