class ApiError(Exception):
    code = 400
    description = "Hubo un error inesperado. Intente más tarde."


class ValidationApiError(ApiError):
    code = 400
    description = "Faltan campos requeridos."


class InvalidFormatError(ApiError):
    code = 400
    description = "Formato de campo inválido."


class ProductAlreadyExistsError(ApiError):
    code = 412
    description = "El producto a registrar ya existe."


class ProductNotExistsError(ApiError):
    code = 404
    description = "El producto no existe."
