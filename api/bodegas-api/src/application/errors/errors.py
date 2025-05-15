class ApiError(Exception):
    code = 400
    description = "unexpected error occurred. please try again later."


class ValidationApiError(ApiError):
    code = 400
    description = "required fields are missing."


class InvalidFormatError(ApiError):
    code = 400
    description = "invalid field format."


class InvalidTokenError(ApiError):
    code = 401
    description = "Unauthorized."


class ForbiddenError(ApiError):
    code = 403
    description = "Forbidden."


class ResourceNotFoundError(ApiError):
    code = 404
    description = "requested resource does not exist."


class WarehouseNotFoundError(ApiError):
    code = 404
    description = "requested warehouse does not exist in the system."


class WarehouseStockItemNotFoundError(ApiError):
    code = 404
    description = "requested stock item does not exist in the system."


class DuplicateWarehouseError(ApiError):
    code = 412
    description = "a warehouse with this name already exists. please enter another name."


class DuplicateWarehouseStockItemError(ApiError):
    code = 412
    description = "a stock item with this code already exists. please enter another code."
