class ApiError(Exception):
    code = 400
    description = "Hubo un error inesperado. Intente más tarde."


class InternalServerError(ApiError):
    code = 500
    description = "Error interno del servidor. Intente más tarde"


class ValidationApiError(ApiError):
    def __init__(self, message=None):
        super().__init__(message)
        self.code = 400
        self.description = message or "Error de validación de datos."


class InvalidFormatError(ApiError):
    def __init__(self, message=None):
        super().__init__(message)
        self.code = 400
        self.description = message or "Formato de campo inválido."


class OrderNotExistsError(ApiError):
    code = 404
    description = "La orden consultada no existe."

class OrdersNotFoundError(ApiError):
    code = 404
    description = "No se encontraron órdenes para el cliente consultado."