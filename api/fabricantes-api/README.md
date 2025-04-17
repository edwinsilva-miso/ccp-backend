# Fabricantes API

Este servicio proporciona una API para la gestión de fabricantes en el sistema CCP.

## Instalación

### Requisitos previos
- Python 3.10+
- PostgreSQL
- Docker y Docker Compose (opcional)

### Configuración local

1. Clonar el repositorio y navegar al directorio del servicio:

```bash
cd api/fabricantes-api
```

2. Crear un entorno virtual e instalar dependencias:

```bash
pip install pipenv
pipenv install
pipenv shell
```

3. Configurar variables de entorno:
   - Copiar `.env.development` a `.env` y ajustar según sea necesario

4. Iniciar la base de datos PostgreSQL:
   - Puede usar el servicio `manufacturers_db` definido en el `docker-compose.yml`
   - O configurar PostgreSQL localmente en el puerto 5433

5. Ejecutar migraciones y levantar el servicio:

```bash
# Aplicar migraciones si están configuradas
flask run
```

### Despliegue con Docker

Para ejecutar el servicio como parte del ecosistema completo:

```bash
docker-compose up -d manufacturers-api
```

## Uso

El servicio de Fabricantes proporciona endpoints para:
- Listar todos los fabricantes
- Obtener detalles de un fabricante específico
- Crear nuevos fabricantes
- Actualizar información de fabricantes existentes
- Eliminar fabricantes

## Endpoints

### GET /api/v1/manufacturers/
Obtiene todos los fabricantes registrados.

**Respuesta exitosa**: `200 OK`
```json
[
  {
    "id": "123",
    "name": "Fabricante Ejemplo",
    "address": "Calle Principal 123",
    "phone": "123-456-7890",
    "email": "contacto@fabricante.com",
    "legal_representative": "Juan Pérez",
    "country": "Colombia",
    "status": "ACTIVO"
  }
]
```

### GET /api/v1/manufacturers/{id}
Obtiene información detallada de un fabricante específico.

**Respuesta exitosa**: `200 OK`
```json
{
  "id": "123",
  "name": "Fabricante Ejemplo",
  "address": "Calle Principal 123",
  "phone": "123-456-7890",
  "email": "contacto@fabricante.com",
  "legal_representative": "Juan Pérez",
  "country": "Colombia",
  "status": "ACTIVO"
}
```

### POST /api/v1/manufacturers/
Crea un nuevo fabricante.

**Cuerpo de la solicitud**:
```json
{
  "name": "Nuevo Fabricante",
  "address": "Calle 456",
  "phone": "987-654-3210",
  "email": "nuevo@fabricante.com",
  "legal_representative": "Ana Gómez",
  "country": "México"
}
```

**Respuesta exitosa**: `201 Created`
```json
{
  "id": "nuevo-id",
  "name": "Nuevo Fabricante",
  "address": "Calle 456",
  "phone": "987-654-3210",
  "email": "nuevo@fabricante.com",
  "legal_representative": "Ana Gómez",
  "country": "México",
  "status": "ACTIVO"
}
```

### PUT /api/v1/manufacturers/{id}
Actualiza la información de un fabricante existente.

**Cuerpo de la solicitud**:
```json
{
  "name": "Fabricante Actualizado",
  "address": "Nueva Dirección",
  "phone": "111-222-3333",
  "email": "actualizado@fabricante.com",
  "legal_representative": "Carlos López",
  "country": "Argentina",
  "status": "INACTIVO"
}
```

**Respuesta exitosa**: `200 OK`
```json
{
  "id": "123",
  "name": "Fabricante Actualizado",
  "address": "Nueva Dirección",
  "phone": "111-222-3333",
  "email": "actualizado@fabricante.com",
  "legal_representative": "Carlos López",
  "country": "Argentina",
  "status": "INACTIVO"
}
```

### DELETE /api/v1/manufacturers/{id}
Elimina un fabricante existente.

**Respuesta exitosa**: `204 No Content`

## Autenticación

Todos los endpoints requieren un token JWT válido en el encabezado de autorización:

```
Authorization: Bearer <token>
```