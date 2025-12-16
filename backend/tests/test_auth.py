import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_login_flow(client: AsyncClient, admin_token):
    # Admin token fixture already verifies login success internally, 
    # but let's test explicit login failure and success.
    
    # Success
    response = await client.post("/token", data={"username": "pytest_admin", "password": "admin123"})
    assert response.status_code == 200
    assert "access_token" in response.json()

    # Failure
    response = await client.post("/token", data={"username": "pytest_admin", "password": "wrongpassword"})
    assert response.status_code == 400 or response.status_code == 401

@pytest.mark.asyncio
async def test_protected_route_access(client: AsyncClient, admin_token):
    # Access as admin
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await client.get("/users/", headers=headers)
    assert response.status_code == 200

    # Access without token
    response = await client.get("/users/")
    assert response.status_code == 401
