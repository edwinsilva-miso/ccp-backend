# Users API

## Purpose
This microservice manages user authentication and authorization for the application ecosystem. It handles:
- User registration and management
- Role-based access control
- Password encryption and validation

## Installation

### Prerequisites
- Python 3.11+
- pip
- pipenv
- PostgreSQL

### Setup
1. Clone the repository
2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows
```

3. Install dependencies using pipenv:
```bash
pipenv install
```

## Environment Variables
Create a `.env` file with the following variables:

```ini
# Database
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=users_db

# Application
FLASK_APP=src/main.py
FLASK_ENV=development
SECRET_KEY=your_secret_key
```

## Running Tests

### Unit Tests
Run all tests:
```bash
cd api/usuarios-api
python -m pytest
```

### Coverage Tests
Run tests with coverage report:
```bash
cd api/usuarios-api
python -m pytest --cov-config=pytest.ini --cov=src --cov-report=term-missing
```

Generate HTML coverage report:
```bash
python -m pytest --cov-config=pytest.ini --cov=src --cov-report=html
```

The HTML report will be available in the `htmlcov` directory.

Note: Coverage configuration excludes:
- Domain entities (`src/domain/entities/*`)
- Constants (`src/domain/utils/constants.py`)
- Infrastructure code (`src/infrastructure/*`)

## API Endpoints

### Health Check
- **URL**: `/health`
- **Method**: `GET`
- **Success Response**: `{"status": "UP"}`

### Create User
- **URL**: `/api/v1/users/`
- **Method**: `POST`
- **Payload**:
```json
{
    "name": "string",
    "phone": "string",
    "email": "string",
    "password": "string",
    "role": "CLIENTE"
}
```
- **Success Response**: `201 Created`
```json
{
    "id": "user-uuid"
}
```

## Project Structure
```
src/
├── application/       # Use cases and business logic
├── domain/           # Business entities and rules
├── infrastructure/   # External dependencies (DB, external services)
└── interface/        # API endpoints and controllers
```