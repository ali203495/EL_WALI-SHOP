import requests
import sys

BASE_URL = "http://localhost:8000"

def verify_wishlist_backend():
    print("🚀 Starting Wishlist Backend Verification...")

    # 1. Login as Admin to get token
    print("1. Logging in...")
    resp = requests.post(f"{BASE_URL}/token", data={"username": "abdelaali", "password": "acbd1234!@#$"})
    if resp.status_code != 200:
        print(f"❌ Login failed: {resp.text}")
        return
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("✅ Logged in.")

    # 2. Get Product ID (assume we have one from seed)
    print("2. Fetching products...")
    resp = requests.get(f"{BASE_URL}/products/", headers=headers)
    if resp.status_code != 200:
        print(f"❌ Failed to fetch products: {resp.text}")
        return
    products = resp.json()
    if not products:
        print("❌ No products found to add to wishlist.")
        return
    product_id = products[0]['id']
    print(f"✅ Found product ID: {product_id}")

    # 3. Add to Wishlist
    print(f"3. Adding product {product_id} to wishlist...")
    resp = requests.post(f"{BASE_URL}/wishlist/", json={"product_id": product_id}, headers=headers)
    if resp.status_code == 200:
        print("✅ Added to wishlist.")
    elif resp.status_code == 400 and "already" in resp.text:
        print("ℹ️ Product already in wishlist (expected if re-running).")
    else:
        print(f"❌ Failed to add to wishlist: {resp.text}")
        return

    # 4. Get Wishlist
    print("4. Fetching wishlist...")
    resp = requests.get(f"{BASE_URL}/wishlist/", headers=headers)
    if resp.status_code != 200:
        print(f"❌ Failed to fetch wishlist: {resp.text}")
        return
    wishlist = resp.json()
    print(f"✅ Wishlist items: {len(wishlist)}")
    
    found = any(item['product']['id'] == product_id for item in wishlist)
    if not found:
        print("❌ Added product not found in wishlist!")
        return
    print("✅ Product confirmed in wishlist.")

    # 5. Remove from Wishlist
    print(f"5. Removing product {product_id} from wishlist...")
    resp = requests.delete(f"{BASE_URL}/wishlist/{product_id}", headers=headers)
    if resp.status_code != 200:
        print(f"❌ Failed to remove from wishlist: {resp.text}")
        return
    print("✅ Removed from wishlist.")

    # 6. Verify Removal
    print("6. Verifying removal...")
    resp = requests.get(f"{BASE_URL}/wishlist/", headers=headers)
    wishlist = resp.json()
    found = any(item['product']['id'] == product_id for item in wishlist)
    if found:
        print("❌ Product still in wishlist after removal!")
    else:
        print("✅ Product successfully removed.")

if __name__ == "__main__":
    verify_wishlist_backend()
