# Mobile BFF Service

BFF (Backend for Frontend) service specifically designed for mobile clients. This service acts as an intermediary layer between the mobile frontend and the backend services, providing optimized endpoints for mobile applications.

## Description

The Mobile BFF service:
- Runs on Flask
- Provides API endpoints optimized for mobile clients
- Communicates with the Users API service
- Handles user registration and authentication
- Runs on port 5001 (mapped to container port 5000)

## Prerequisites

- Python 3.11.6
- pipenv
- Docker and Docker Compose

## Installation

### Local Development

1. Install dependencies:
```bash
pipenv install
```

2. Activate virtual environment:
```bash
pipenv shell
```

3. Set environment variables:
```bash
export FLASK_APP=src/main.py
export USERS_API_URL=http://localhost:5100
```

### Using Docker

Build the container:
```bash
docker build -t mobile-bff .
```

## Running the Service

### Local Development

```bash
flask run --port 5001
```

### Using Docker Compose

From the root directory:
```bash
docker-compose up mobile-bff
```

## API Endpoints

### User Registration
- **URL**: `/bff/v1/mobile/users/`
- **Method**: POST
- **Description**: Register a new user

#### Request Example
```bash
curl -X POST http://localhost:5001/bff/v1/mobile/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john.doe@example.com",
    "phone": "3153334455",
    "password": "pass123",
    "role": "CLIENTE"
  }'
```

#### Successful Response (201 Created)
```json
{
  "id": "user-uuid"
}
```

#### Error Responses
- **400 Bad Request**: Missing required fields
```json
{
  "msg": "Missing required fields"
}
```

- **412 Precondition Failed**: User already exists
```json
{
  "msg": "User already exists"
}
```

- **500 Internal Server Error**: Server error
```json
{
  "error": "Internal server error"
}
```

## Testing

Run tests using pytest:
```bash
pipenv run pytest
```

## Project Structure

```
mobile-bff/
├── src/
│   ├── adapters/        # External service adapters
│   ├── blueprints/      # API route definitions
│   └── main.py         # Application entry point
├── tests/              # Unit tests
├── Dockerfile
└── Pipfile            # Dependencies
```

## Environment Variables

- `FLASK_APP`: Application entry point (default: src/main.py)
- `USERS_API_URL`: Users API service URL (default: http://users-api:5000)