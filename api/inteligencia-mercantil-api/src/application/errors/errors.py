class ApiError(Exception):
    code = 400
    description = "Hubo un error inesperado. Intente más tarde."


class ValidationApiError(ApiError):
    code = 400
    description = "Faltan campos requeridos."


class InvalidFormatError(ApiError):
    code = 400
    description = "Formato de campo inválido."


class UserAlreadyExistsError(ApiError):
    code = 412
    description = "El registro ya existe."


class UserNotExistsError(ApiError):
    code = 404
    description = "El usuario no existe."


class InvalidTokenError(ApiError):
    code = 401
    description = "Unauthorized."


class ForbiddenError(ApiError):
    code = 403
    description = "Forbidden."