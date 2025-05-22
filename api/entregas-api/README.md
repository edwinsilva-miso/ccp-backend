# Deliveries API

A microservice for managing deliveries between sellers and customers.

## Features

- Sellers can create, read, update, and delete deliveries
- Sellers can add status updates to deliveries
- Customers can view their deliveries and check status updates

## Setup

### Prerequisites

- Python 3.11+
- PostgreSQL

### Installation

1. Clone the repository
2. Install dependencies:
   ```
   pipenv install
   ```
3. Create a `.env.development` file with your configuration (see `.env.development` for an example)
4. Create the PostgreSQL database:
   ```
   createdb entregas_dev
   ```

### Running the Application

```
pipenv run python src/main.py
```

The API will be available at http://localhost:5000

## API Documentation

### Seller Endpoints

#### Create a Delivery

```
POST /api/seller/deliveries
```

Request body:
```json
{
  "customer_id": 123,
  "seller_id": 456,
  "description": "Package with electronics",
  "estimated_delivery_date": "2023-12-25T12:00:00",
  "initial_status": "created",
  "status_description": "Order received"
}
```

#### Get Seller Deliveries

```
GET /api/seller/deliveries?seller_id=456
```

#### Get a Specific Delivery

```
GET /api/seller/deliveries/1?seller_id=456
```

#### Update a Delivery

```
PUT /api/seller/deliveries/1
```

Request body:
```json
{
  "seller_id": 456,
  "description": "Updated package description",
  "estimated_delivery_date": "2023-12-26T12:00:00"
}
```

#### Delete a Delivery

```
DELETE /api/seller/deliveries/1?seller_id=456
```

#### Add a Status Update

```
POST /api/seller/deliveries/1/status
```

Request body:
```json
{
  "seller_id": 456,
  "status": "in_transit",
  "description": "Package is on the way"
}
```

### Customer Endpoints

#### Get Customer Deliveries

```
GET /api/customer/deliveries?customer_id=123
```

#### Get a Specific Delivery

```
GET /api/customer/deliveries/1?customer_id=123
```

## Testing

For testing, the application uses SQLite instead of PostgreSQL. To run tests:

```
pipenv run pytest
```
