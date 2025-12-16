import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_category_list(client: AsyncClient, admin_token):
    # Create a category to ensure list isn't empty
    headers = {"Authorization": f"Bearer {admin_token}"}
    await client.post(
        "/categories/",
        json={"name": "Integration Test Cat"},
        headers=headers
    )

    response = await client.get("/categories/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert any(c["name"] == "Integration Test Cat" for c in data)
