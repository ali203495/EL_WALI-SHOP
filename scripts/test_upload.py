import requests
import os

def test_upload():
    # Create dummy image
    dummy_path = "test_image.txt"
    with open(dummy_path, "w") as f:
        f.write("dummy image content")
        
    url = "http://localhost:8000/upload/"
    
    try:
        with open(dummy_path, "rb") as f:
            files = {"file": ("test_image.txt", f, "text/plain")}
            print("🚀 Uploading file...")
            response = requests.post(url, files=files)
            
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            file_url = data.get("url")
            print(f"✅ Upload success! URL: {file_url}")
            
            # Verify access
            print("🔍 Verifying access...")
            res_get = requests.get(file_url)
            if res_get.status_code == 200:
                print("✅ File verified accessible!")
            else:
                print(f"❌ Failed to access file: {res_get.status_code}")
        else:
            print("❌ Upload failed")
            
    finally:
        if os.path.exists(dummy_path):
            os.remove(dummy_path)

if __name__ == "__main__":
    test_upload()
