
import urllib.request
import urllib.parse
import json
import uuid

BASE_URL = "http://localhost:8000"
USERNAME = "abdelaali"
PASSWORD = "abcd1234!@#$"

def login():
    data = urllib.parse.urlencode({
        "username": USERNAME,
        "password": PASSWORD
    }).encode()
    req = urllib.request.Request(f"{BASE_URL}/token", data=data, method="POST")
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())["access_token"]

def create_category(token):
    cat_name = f"TestCat_{uuid.uuid4().hex[:8]}"
    data = json.dumps({"name": cat_name}).encode()
    req = urllib.request.Request(f"{BASE_URL}/categories/", data=data, method="POST")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

def create_product(token, cat_id):
    prod_name = f"TestProd_{uuid.uuid4().hex[:8]}"
    data = json.dumps({
        "name": prod_name,
        "price": 100.0,
        "stock": 10,
        "category_id": cat_id,
        "description": "Initial Desc"
    }).encode()
    req = urllib.request.Request(f"{BASE_URL}/products/", data=data, method="POST")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

def update_product(token, prod_id, new_name):
    data = json.dumps({
        "name": new_name,
        # Only sending name to test partial update
    }).encode()
    req = urllib.request.Request(f"{BASE_URL}/products/{prod_id}", data=data, method="PUT")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

def main():
    try:
        print("Logging in...")
        token = login()
        print("Logged in.")
        
        print("Creating Category...")
        cat = create_category(token)
        print(f"Category created: {cat['id']}")
        
        print("Creating Product...")
        prod = create_product(token, cat['id'])
        print(f"Product created: {prod['id']} - Name: {prod['name']}")
        
        print("Updating Product...")
        new_name = prod['name'] + "_UPDATED"
        updated_prod = update_product(token, prod['id'], new_name)
        print(f"Product updated: {updated_prod['id']} - Name: {updated_prod['name']}")
        
        if updated_prod['name'] == new_name:
            print("SUCCESS: Product update verified.")
        else:
            print("FAILURE: Name mismatch.")
            
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    main()
