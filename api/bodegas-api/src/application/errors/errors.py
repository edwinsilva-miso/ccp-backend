class ApiError(Exception):
    code = 400
    description = "Hubo un error inesperado. Intente más tarde."


class ValidationApiError(ApiError):
    code = 400
    description = "Faltan campos requeridos."


class InvalidFormatError(ApiError):
    code = 400
    description = "Formato de campo inválido."


class InvalidTokenError(ApiError):
    code = 401
    description = "Unauthorized."


class ForbiddenError(ApiError):
    code = 403
    description = "Forbidden."


class ResourceNotFoundError(ApiError):
    code = 404
    description = "El recurso solicitado no existe."


class WarehouseNotFoundError(ApiError):
    code = 404
    description = "La bodega solicitada no existe en el sistema."


class WarehouseStockItemNotFoundError(ApiError):
    code = 404
    description = "El artículo de stock solicitado no existe en el sistema."


class DuplicateWarehouseError(ApiError):
    code = 412
    description = "Ya existe una bodega con ese nombre. Por favor ingrese otro nombre."


class DuplicateWarehouseStockItemError(ApiError):
    code = 412
    description = "Ya existe un artículo de stock con ese código. Por favor ingrese otro código."