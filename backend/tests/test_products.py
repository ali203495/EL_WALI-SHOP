import pytest
from httpx import AsyncClient

# Test Data
product_data = {
    "name": "Test Product",
    "description": "A product for testing",
    "price": 99.99,
    "stock": 10,
    "category_id": 1
}

@pytest.mark.asyncio
async def test_create_category_for_product(client: AsyncClient, admin_token):
    # Ensure a category exists first (id 1)
    response = await client.post(
        "/categories/",
        json={"name": "Test Category"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code in [200, 201]

@pytest.mark.asyncio
async def test_product_lifecycle(client: AsyncClient, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    # 1. Create Product
    response = await client.post("/products/", json=product_data, headers=headers)
    assert response.status_code == 200
    p_data = response.json()
    assert p_data["name"] == product_data["name"]
    product_id = p_data["id"]

    # 2. Read Product
    response = await client.get(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["id"] == product_id

    # 3. Update Product
    update_data = {"price": 150.00}
    response = await client.put(f"/products/{product_id}", json=update_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["price"] == 150.00

    # 4. Delete Product
    response = await client.delete(f"/products/{product_id}", headers=headers)
    assert response.status_code == 200
    
    # 5. Verify Deletion
    response = await client.get(f"/products/{product_id}")
    assert response.status_code == 404
