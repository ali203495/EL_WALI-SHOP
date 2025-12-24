
import asyncio
import os
import sys

# Manual .env parser
try:
    with open(".env", "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, value = line.split("=", 1)
                os.environ[key.strip()] = value.strip()
except Exception as e:
    print(f"Warning: Could not read .env file: {e}")

from services.facebook_post import facebook_service

class MockProduct:
    def __init__(self):
        self.name = "Test Product (Verification)"
        self.description = "This is a test post to verify the Facebook Auto-Post integration."
        self.price = 999.0
        self.image_url = None # Test text only first

async def test():
    print(f"Testing with Page ID: {facebook_service.page_id}")
    # Re-initialize service to pick up env vars if they were set after import (unlikely, but class init happens at import time usually)
    # Actually, the service instance 'facebook_service' was created at import time. 
    # If we set os.environ *after* import (which we did here, oops), the class might have already read the old env (or None).
    # We should re-instantiate the service.
    
    facebook_service.page_id = os.getenv("FACEBOOK_PAGE_ID")
    facebook_service.access_token = os.getenv("FACEBOOK_ACCESS_TOKEN")

    if not facebook_service.access_token:
        print("Error: No Access Token found in env.")
        print("Please ensure FACEBOOK_ACCESS_TOKEN is set in .env")
        return

    print("Sending test post...")
    await facebook_service.post_product(MockProduct())
    print("Test finished.")

if __name__ == "__main__":
    asyncio.run(test())
