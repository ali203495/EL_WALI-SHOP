import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_super_admin_capabilities(client: AsyncClient, admin_token, regular_user_token):
    # admin_token is SUPER ADMIN in conftest
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    user_headers = {"Authorization": f"Bearer {regular_user_token}"}
    
    # 1. Create Sub Admin using Super Admin
    sub_admin_data = {
        "username": "sub_admin",
        "password": "subpassword",
        "email": "sub@example.com",
        "first_name": "Sub",
        "last_name": "Admin",
        "phone_number": "666666",
        "is_admin": True
    }
    response = await client.post("/users/", json=sub_admin_data, headers=admin_headers)
    assert response.status_code == 200
    sub_id = response.json()["id"]

    # 2. Verify Regular User cannot create users (if public reg is disabled or if endpoint is protected)
    # The endpoint /users/ for creation usually depends on config. 
    # But let's test deleting another user which is definitely restricted.
    
    response = await client.delete(f"/users/{sub_id}", headers=user_headers)
    assert response.status_code == 403 or response.status_code == 401

    # 3. Cleanup
    await client.delete(f"/users/{sub_id}", headers=admin_headers)
