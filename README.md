# RESTful API for E-Commerce Platform

## Overview
This project is a production-ready RESTful API for an e-commerce platform built with FastAPI, using PostgreSQL as the database and Docker for containerization.

## Features
- Product management (Add, Retrieve)
- Order processing with stock validation
- PostgreSQL as the database backend
- Fully Dockerized for easy deployment
- Unit and Integration tests using Pytest
- OpenAPI Documentation available via Swagger UI
- Secured Api's using X-API-KEY

## Setup Instructions

### Prerequisites
- Docker & Docker Compose
- Python 3.9+

### Running the Application
1. Clone repository:
   ```bash
   git clone https://github.com/arjitsrivastava007/ecommerce_platform.git
   cd ecommerce_platform
   ```
2. Build and run the application using Docker Compose:
   ```bash
   docker-compose up -d
   ```
3. Stop application
    ```bash
   docker-compose down
   ```
4. Access the API:
   - Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
   - Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Running Tests
To run unit and integration tests:
   - Login to docker container
   - docker exec -it <container_id> bash
   - Run below command
```bash
pytest
```

## API Endpoints
X-API-KEY is present in .env and .env_local file, which is required in swagger to make any api call
### Products
- `GET /v1/ecommerce/products` - Retrieve all products
- `POST /v1/ecommerce/products` - Add a new product

### Orders
- `POST /v1/ecommerce/orders` - Place an order

# Future Developments
   - Improving performance of order create Api
   - Partitioning postgresql for huge dataset
