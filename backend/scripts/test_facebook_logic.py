import asyncio
import os
from unittest.mock import MagicMock, patch

# Mock env vars
os.environ["FACEBOOK_PAGE_ID"] = "123"
os.environ["FACEBOOK_ACCESS_TOKEN"] = "abc"

from services.facebook_post import FacebookPostService

async def test_facebook_logic():
    service = FacebookPostService()
    
    # Mock Product
    class MockProduct:
        def __init__(self, name, description, price, image_url):
            self.name = name
            self.description = description
            self.price = price
            self.image_url = image_url

    print("--- Test 1: Public Image URL ---")
    p1 = MockProduct("Test 1", "Desc", 100, "https://example.com/image.jpg")
    
    with patch("httpx.AsyncClient.post") as mock_post:
        mock_post.return_value = MagicMock(status_code=200, json=lambda: {"id": "fb_post_id_1"})
        await service.post_product(p1)
        
        # Verify it hit the photos endpoint
        args, kwargs = mock_post.call_args
        if "photos" in args[0]:
            print("PASS: Public URL used /photos endpoint")
        else:
            print(f"FAIL: Expected /photos, got {args[0]}")

    print("\n--- Test 2: Local Image URL (Fallback) ---")
    p2 = MockProduct("Test 2", "Desc", 200, "/uploads/local.jpg")
    
    with patch("httpx.AsyncClient.post") as mock_post:
        mock_post.return_value = MagicMock(status_code=200, json=lambda: {"id": "fb_post_id_2"})
        await service.post_product(p2)
        
        # Verify it hit the feed endpoint (text only)
        args, kwargs = mock_post.call_args
        if "feed" in args[0]:
            print("PASS: Local URL fallback used /feed endpoint")
        else:
            print(f"FAIL: Expected /feed, got {args[0]}")

if __name__ == "__main__":
    asyncio.run(test_facebook_logic())
