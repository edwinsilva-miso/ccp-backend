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

### Products Endpoints

#### Get All Products
- **URL**: `/bff/v1/mobile/products/`
- **Method**: GET
- **Description**: Retrieve a list of all products.

##### Request Headers
- `Authorization`: Bearer token (required)

##### Successful Response (200 OK)
```json
[
  {
    "id": "abc123",
    "name": "Product 1",
    "price": 99.99
  },
  {
    "id": "def456",
    "name": "Product 2",
    "price": 149.99
  }
]
```

##### Error Responses
- **401 Unauthorized**: Missing or invalid token
```json
{
  "msg": "Unauthorized"
}
```

---

#### Get Product by ID
- **URL**: `/bff/v1/mobile/products/<product_id>`
- **Method**: GET
- **Description**: Retrieve details of a specific product by its ID.

##### Request Headers
- `Authorization`: Bearer token (required)

##### Successful Response (200 OK)
```json
{
  "id": "abc123",
  "name": "Test Product",
  "brand": "Test Brand",
  "manufacturerId": "manufacturer_test",
  "description": "Test Description",
  "price": 199.99
}
```

##### Error Responses
- **401 Unauthorized**: Missing or invalid token
```json
{
  "msg": "Unauthorized"
}
```
- **404 Not Found**: Product not found
```json
{
  "msg": "Product not found"
}
```

---

#### Create Product
- **URL**: `/bff/v1/mobile/products/`
- **Method**: POST
- **Description**: Create a new product.

##### Request Headers
- `Authorization`: Bearer token (required)
- `Content-Type`: application/json

##### Request Body
```json
{
  "name": "Test Product",
  "brand": "Test Brand",
  "manufacturerId": "manufacturer_test",
  "description": "Test Description",
  "details": {"color": "gray", "size": "9.5"},
  "storageConditions": "Clean site",
  "price": 199.99,
  "currency": "USD",
  "deliveryTime": 5,
  "images": ["image1.png", "image2.png"]
}
```

##### Successful Response (201 Created)
```json
{
  "id": "abc123",
  "msg": "Product created successfully"
}
```

##### Error Responses
- **400 Bad Request**: Missing required fields
```json
{
  "msg": "Missing required fields."
}
```
- **401 Unauthorized**: Missing or invalid token
```json
{
  "msg": "Unauthorized"
}
```

---

#### Update Product
- **URL**: `/bff/v1/mobile/products/<product_id>`
- **Method**: PUT
- **Description**: Update an existing product.

##### Request Headers
- `Authorization`: Bearer token (required)
- `Content-Type`: application/json

##### Request Body
Same as the **Create Product** request body.

##### Successful Response (200 OK)
```json
{
  "msg": "Product updated successfully"
}
```

##### Error Responses
- **400 Bad Request**: Missing required fields
```json
{
  "msg": "Missing required fields."
}
```
- **401 Unauthorized**: Missing or invalid token
```json
{
  "msg": "Unauthorized"
}
```
- **404 Not Found**: Product not found
```json
{
  "msg": "Product not found"
}
```

---

#### Delete Product
- **URL**: `/bff/v1/mobile/products/<product_id>`
- **Method**: DELETE
- **Description**: Delete a product by its ID.

##### Request Headers
- `Authorization`: Bearer token (required)

##### Successful Response (200 OK)
```json
{
  "msg": "Product deleted successfully"
}
```

##### Error Responses
- **401 Unauthorized**: Missing or invalid token
```json
{
  "msg": "Unauthorized"
}
```
- **404 Not Found**: Product not found
```json
{
  "msg": "Product not found"
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
- `PRODUCTS_API_URL`: Products API service URL (default: http://products-api:5000)