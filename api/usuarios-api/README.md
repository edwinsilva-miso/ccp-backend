# Usuarios

## Descripción
Este módulo permite gestionar los usuarios de la aplicación. Permite crear, editar y eliminar usuarios, así como asignarles roles y permisos.

### Estructura de la base de datos
La tabla `usuarios` tiene la siguiente estructura:

```sql
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    rol VARCHAR(50),
    permisos JSONB,
    activo BOOLEAN DEFAULT true,
    fecha_creacion TIMESTAMP DEFAULT now(),
    fecha_modificacion TIMESTAMP DEFAULT now(),
    fecha_ultimo_acceso TIMESTAMP DEFAULT now()
);
```

## Endpoints
### Crear usuario
- **URL**: `/usuarios`
- **Método**: `POST`
- **Descripción**: Crea un nuevo usuario.
- **Parámetros**:
  - `nombre`: Nombre del usuario (requerido).
  - `email`: Correo electrónico del usuario (requerido).
  - `password`: Contraseña del usuario (requerido).
  - `rol`: Rol del usuario (opcional).
  - `permisos`: Lista de permisos del usuario (opcional).
  - `activo`: Estado del usuario (opcional, por defecto `true`).
  - `fecha_creacion`: Fecha de creación del usuario (opcional, por defecto `now()`).
  - `fecha_modificacion`: Fecha de modificación del usuario (opcional, por defecto `now()`).
  - `fecha_ultimo_acceso`: Fecha del último acceso del usuario (opcional, por defecto `now()`).

- **Respuesta**:
  - `201 Created`: Usuario creado exitosamente.
  - `400 Bad Request`: Error en la solicitud (por ejemplo, falta de parámetros requeridos).
  - `500 Internal Server Error`: Error interno del servidor.

## Curl
```bash
```
