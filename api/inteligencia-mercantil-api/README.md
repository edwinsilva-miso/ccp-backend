# Transports API
# Video Processing Microservice

This microservice handles video uploads, stores them in Google Cloud Storage, processes them with Vertex AI, and stores metadata in a PostgreSQL database.

## Features

- Upload videos about places
- Store videos in Google Cloud Storage (GCS)
- Process videos with Vertex AI to analyze product placement opportunities
- Track video processing status in a PostgreSQL database
- Query video processing status and results

## Architecture

This project follows the hexagonal architecture (also known as ports and adapters):

- **Domain Layer**: Contains the core business logic and entities
- **Application Layer**: Orchestrates the use cases and business workflows
- **Infrastructure Layer**: Provides implementations for external services
- **Interface Layer**: Handles HTTP requests and responses

## API Endpoints

### Upload a Video
TODO
