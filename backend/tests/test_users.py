import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_user_crud(client: AsyncClient, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    # 1. Create User
    user_data = {
        "username": "crud_user",
        "password": "password123",
        "email": "crud@example.com",
        "first_name": "Crud",
        "last_name": "User",
        "phone_number": "555555",
        "is_admin": False
    }
    response = await client.post("/users/", json=user_data, headers=headers)
    assert response.status_code == 200
    u_data = response.json()
    user_id = u_data["id"]

    # 2. Update User
    update_data = {"is_admin": True}
    response = await client.put(f"/users/{user_id}", json=update_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["is_admin"] is True

    # 3. Delete User
    response = await client.delete(f"/users/{user_id}", headers=headers)
    assert response.status_code == 200
    
    # Verify deletion by trying to get (if get endpoint exists) OR by listing
    # Assuming list endpoint filters or shows all
    # Or just try delete again (404)
    response = await client.delete(f"/users/{user_id}", headers=headers)
    assert response.status_code == 404
