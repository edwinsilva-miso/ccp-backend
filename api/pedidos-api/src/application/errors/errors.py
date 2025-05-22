class ApiError(Exception):
    code = 400
    description = "Hubo un error inesperado. Intente más tarde."


class ValidationApiError(ApiError):
    code = 400
    description = "Faltan campos requeridos."


class OrdersNotFoundError(ApiError):
    code = 404
    description = "No se encontraron pedidos."


class OrderNotExistsError(ApiError):
    code = 404
    description = "El pedido consultado no existe."
