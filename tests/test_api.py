import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# Define test database connection URL
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
headers = {
    "Content-Type": "application/json",
    "X-API-KEY": os.environ.get("API_KEY")
}


@pytest.mark.asyncio
async def test_get_products_no_product(client):
    """Test retrieving all products API"""
    response = client.get("/v1/ecommerce/products", headers=headers)
    assert response.status_code == 404
    assert response.json()["message"] == "No products available"


@pytest.mark.asyncio
async def test_create_product(client):
    """Test product creation API"""
    response = client.post("/v1/ecommerce/products", headers=headers,
                           json={"name": "Phone", "description": "iPhone 15", "price": 1200, "stock": 10})
    assert response.status_code == 200
    assert response.json()["name"] == "Phone"


@pytest.mark.asyncio
async def test_get_products(client):
    """Test retrieving all products API"""
    response = client.get("/v1/ecommerce/products", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_create_product_negative_price(client):
    """Test product creation API"""
    response = client.post("/v1/ecommerce/products", headers=headers,
                           json={"name": "Phone", "description": "iPhone 15", "price": -1200, "stock": 10})
    assert response.status_code == 400
    assert response.json()["message"] == "Price must be greater than zero"


@pytest.mark.asyncio
async def test_create_product_negative_stock(client):
    """Test product creation API"""
    response = client.post("/v1/ecommerce/products", headers=headers,
                           json={"name": "Phone", "description": "iPhone 15", "price": 1200, "stock": -1})
    assert response.status_code == 400
    assert response.json()["message"] == "Stock cannot be negative"


@pytest.mark.asyncio
async def test_create_order_success(client):
    """Test order creation API success case"""
    # First, create a product
    product = client.post("/v1/ecommerce/products", headers=headers,
                json={"name": "Laptop", "description": "Gaming Laptop", "price": 1000, "stock": 5})
    assert product.status_code == 200
    product_details = product.json()

    # Now, create an order
    response = client.post("/v1/ecommerce/orders", headers=headers,
                           json={"products": [{"product_id": product_details['id'], "quantity": 1}]})
    assert response.status_code == 200
    assert response.json()["status"] == "placed"


@pytest.mark.asyncio
async def test_create_order_insufficient_stock(client):
    """Test order creation API failure due to insufficient stock"""
    # First, create a product with low stock
    product = client.post("/v1/ecommerce/products", headers=headers,
                json={"name": "Watch", "description": "Smartwatch", "price": 300, "stock": 1})
    assert product.status_code == 200
    product_details = product.json()

    # Now, attempt to place an order with higher quantity
    response = client.post("/v1/ecommerce/orders", headers=headers,
                           json={"products": [{"product_id": product_details['id'], "quantity": 2}]})
    assert response.status_code == 400
    assert "Invalid details" in response.json()["message"]


@pytest.mark.asyncio
async def test_create_order_invalid_product(client):
    """Test order creation API failure due to invalid product id supplied"""

    # place an order with invalid product
    response = client.post("/v1/ecommerce/orders", headers=headers,
                           json={"products": [{"product_id": 100, "quantity": 2}]})
    assert response.status_code == 400
    assert "Invalid details" in response.json()["message"]
