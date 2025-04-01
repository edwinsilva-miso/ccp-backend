# Proyecto CCP

## Capa Backend For Frontend (BFF)

### Descripción
La capa BFF es una capa intermedia entre el frontend y los microservicios. Su objetivo es proporcionar una API optimizada para las necesidades específicas del frontend, evitando que el frontend tenga que interactuar directamente con múltiples microservicios.

### Objetivos
- Proporcionar una API optimizada para el frontend.
- Reducir la complejidad de las interacciones entre el frontend y los microservicios.
- Mejorar el rendimiento al reducir la cantidad de llamadas a los microservicios.
- Facilitar la implementación de cambios en el frontend sin afectar a los microservicios.
- Proporcionar una capa de seguridad adicional entre el frontend y los microservicios.
- Facilitar la implementación de patrones de diseño como GraphQL o RESTful APIs.

### Tecnologías
- Python:
  - Flask: Microframework para construir aplicaciones web.
  - Pydantic: Validación de datos y configuración de modelos.

### BFF incluídos 

- **web-bff**: BFF para la aplicación web.
  - URL de la API: `http://localhost:5000/bff/v1/web/`
- **mobile-bff**: BFF para la aplicación móvil.
  - URL de la API: `http://localhost:5001/bff/v1/mobile/`

### Estructura

```plaintext
.
├── README.md
├── __init__.py
├── mobile-bff
│   ├── Dockerfile
│   ├── Pipfile
│   ├── __init__.py
│   ├── pytest.ini
│   ├── src
│   │   ├── __init__.py
│   │   ├── adapters
│   │   │   └── __init__.py
│   │   ├── blueprints
│   │   │   └── __init__.py
│   │   ├── main.py
│   │   └── utils
│   │       └── __init__.py
│   └── test
│       └── __init__.py
└── web-bff
    ├── Dockerfile
    ├── Pipfile
    ├── Pipfile.lock
    ├── __init__.py
    ├── pytest.ini
    ├── src
    │   ├── __init__.py
    │   ├── adapters
    │   │   └── __init__.py
    │   ├── blueprints
    │   │   └── __init__.py
    │   ├── main.py
    │   └── utils
    │       └── __init__.py
    └── test
        └── __init__.py
```
