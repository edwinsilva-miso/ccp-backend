class ApiError(Exception):
    code = 400
    description = "Hubo un error inesperado. Intente más tarde."


class ValidationApiError(ApiError):
    code = 400
    description = "Faltan campos requeridos."


class InvalidFormatError(ApiError):
    code = 400
    description = "Formato de campo inválido."


class RecordNotExistsError(ApiError):
    code = 404
    description = "El registro de visita de cliente no existe en el sistema."


class ClientAlreadyAssociatedError(ApiError):
    code = 412
    description = "El cliente que intenta asociar ya existe. Por favor ingrese otro cliente."


class InvalidTokenError(ApiError):
    code = 401
    description = "Unauthorized."


class ForbiddenError(ApiError):
    code = 403
    description = "Forbidden."


class ResourceNotFoundError(ApiError):
    code = 404
    description = "El recurso solicitado no existe."
