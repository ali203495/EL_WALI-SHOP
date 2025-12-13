import requests
import sys

BASE_URL = "http://localhost:8000"
ADMIN_USER = "abdelaali"
ADMIN_PASS = "acbd1234!@#$"

def color_print(msg, color="green"):
    colors = {
        "green": "\033[92m",
        "red": "\033[91m",
        "yellow": "\033[93m",
        "reset": "\033[0m"
    }
    print(f"{colors.get(color, '')}{msg}{colors['reset']}")

def login(username, password):
    response = requests.post(f"{BASE_URL}/token", data={"username": username, "password": password})
    if response.status_code == 200:
        return response.json()["access_token"]
    print(f"Login failed: {response.text}")
    return None

def main():
    color_print("Testing Product Management...", "yellow")

    # 1. Login
    token = login(ADMIN_USER, ADMIN_PASS)
    if not token:
        sys.exit(1)
    
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Create Product
    color_print("Creating product...", "yellow")
    product_data = {
        "name": "Test Product",
        "price": 99.99,
        "stock": 10,
        "category_id": 1
    }
    # Ensure category 1 exists or this might fail e.g. if DB is empty
    # Try creating category first just in case
    requests.post(f"{BASE_URL}/categories/", json={"name": "Test Cat"}, headers=headers)
    
    r = requests.post(f"{BASE_URL}/products/", json=product_data, headers=headers)
    if r.status_code != 200:
        color_print(f"Failed to create product: {r.status_code} - {r.text}", "red")
        sys.exit(1)
    
    product_id = r.json()["id"]
    color_print(f"Product created (ID: {product_id})", "green")

    # 3. Update Product
    color_print("Updating product...", "yellow")
    update_data = {"price": 199.99}
    r = requests.put(f"{BASE_URL}/products/{product_id}", json=update_data, headers=headers)
    if r.status_code == 200 and r.json()["price"] == 199.99:
        color_print("Product updated successfully", "green")
    else:
        color_print(f"Failed to update product: {r.status_code} - {r.text}", "red")

    # 4. Delete Product
    color_print("Deleting product...", "yellow")
    r = requests.delete(f"{BASE_URL}/products/{product_id}", headers=headers)
    if r.status_code == 200:
        color_print("Product deleted successfully", "green")
    else:
        color_print(f"Failed to delete product: {r.status_code} - {r.text}", "red")

if __name__ == "__main__":
    main()
