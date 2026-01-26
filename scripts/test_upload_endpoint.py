import asyncio
import os
from httpx import AsyncClient

async def test_upload():
    # Create a dummy file
    filename = "test_image.txt"
    with open(filename, "w") as f:
        f.write("This is a test image content.")

    url = "http://localhost:8000/upload/"
    
    async with AsyncClient() as client:
        try:
            with open(filename, "rb") as f:
                files = {"file": (filename, f, "text/plain")}
                print(f"Uploading to {url}...")
                response = await client.post(url, files=files)
                
            print(f"Status Code: {response.status_code}")
            if response.status_code == 200:
                print(f"Response: {response.json()}")
                print("UPLOAD VERIFICATION PASSED")
            else:
                print(f"Response: {response.text}")
                print("UPLOAD VERIFICATION FAILED")

        except Exception as e:
            print(f"Error: {e}")
        finally:
            if os.path.exists(filename):
                os.remove(filename)

if __name__ == "__main__":
    asyncio.run(test_upload())
