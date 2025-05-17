import logging
from ..model.warehouse_stock_item_model import WarehouseStockItemModel
from ...domain.entities.warehouse_stock_item_dto import WarehouseStockItemDTO

logger = logging.getLogger(__name__)


class WarehouseStockItemMapper:
    """
    Mapper class to convert between WarehouseStockItemDTO and WarehouseStockItemModel.
    """

    @staticmethod
    def to_dto(model: WarehouseStockItemModel) -> WarehouseStockItemDTO:
        """
        Convert a WarehouseStockItemModel to a WarehouseStockItemDTO.
        :param model: WarehouseStockItemModel to convert.
        :return: Converted WarehouseStockItemDTO.
        """
        logger.debug(f"converting warehouse stock item model to dto: {model.__dict__}")
        dto = WarehouseStockItemDTO(
            warehouse_stock_item_id=str(model.warehouse_stock_item_id),
            warehouse_id=str(model.warehouse_id),
            item_id=str(model.item_id),
            bar_code=model.bar_code,
            identification_code=model.identification_code,
            width=model.width,
            height=model.height,
            depth=model.depth,
            weight=model.weight,
            hallway=model.hallway,
            shelf=model.shelf,
            sold=model.sold,
            status=model.status,
            created_at=model.created_at.isoformat() if model.created_at else None,
            updated_at=model.updated_at.isoformat() if model.updated_at else None
        )
        logger.debug(f"successfully converted to dto: {dto.__dict__}")
        return dto

    @staticmethod
    def to_model(dto: WarehouseStockItemDTO) -> WarehouseStockItemModel:
        """
        Convert a WarehouseStockItemDTO to a WarehouseStockItemModel.
        :param dto: WarehouseStockItemDTO to convert.
        :return: Converted WarehouseStockItemModel.
        """
        logger.debug(f"converting warehouse stock item dto to model: {dto.__dict__}")
        model = WarehouseStockItemModel(
            warehouse_stock_item_id=dto.warehouse_stock_item_id,
            warehouse_id=dto.warehouse_id,
            item_id=dto.item_id,
            bar_code=dto.bar_code,
            identification_code=dto.identification_code,
            width=dto.width,
            height=dto.height,
            depth=dto.depth,
            weight=dto.weight,
            hallway=dto.hallway,
            shelf=dto.shelf,
            sold=dto.sold,
            status=dto.status
        )
        logger.debug(f"successfully converted to model: {model.__dict__}")
        return model

    @staticmethod
    def to_dto_list(models: list[WarehouseStockItemModel]) -> list[WarehouseStockItemDTO]:
        """
        Convert a list of WarehouseStockItemModel to a list of WarehouseStockItemDTO.
        :param models: List of WarehouseStockItemModel to convert.
        :return: List of converted WarehouseStockItemDTO.
        """
        logger.debug(f"converting list of {len(models)} warehouse stock item models to dtos")
        dtos = [WarehouseStockItemMapper.to_dto(model) for model in models]
        logger.debug(f"successfully converted {len(dtos)} models to dtos")
        return dtos

    @staticmethod
    def to_model_list(dtos: list[WarehouseStockItemDTO]) -> list[WarehouseStockItemModel]:
        """
        Convert a list of WarehouseStockItemDTO to a list of WarehouseStockItemModel.
        :param dtos: List of WarehouseStockItemDTO to convert.
        :return: List of converted WarehouseStockItemModel.
        """
        logger.debug(f"converting list of {len(dtos)} warehouse stock item dtos to models")
        models = [WarehouseStockItemMapper.to_model(dto) for dto in dtos]
        logger.debug(f"successfully converted {len(models)} dtos to models")
        return models