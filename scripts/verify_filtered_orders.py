import requests

# Test setup
BASE_URL = "http://localhost:8000"
ADMIN_CREDS = {"username": "Abdelaali", "password": "abcd1234!@#$%"}
# We need a normal user. I'll register one if needed or assume one exists.
# Let's register a temp user.
TEMP_USER = {"username": "testuser_orders", "password": "password123", "email": "test@test.com", "first_name": "Test", "last_name": "User"}

def get_token(creds):
    response = requests.post(f"{BASE_URL}/token", data=creds)
    if response.status_code == 200:
        return response.json()["access_token"]
    return None

def test_filtering():
    print("🚀 Starting Order Filtering Test")
    
    # 1. Register User (ignore fail if exists)
    requests.post(f"{BASE_URL}/users/", json=TEMP_USER)
    
    # 2. Login as User
    user_token = get_token({"username": TEMP_USER["username"], "password": TEMP_USER["password"]})
    if not user_token:
        print("❌ Failed to login as user")
        return

    print(f"✅ Logged in as {TEMP_USER['username']}")
    
    # 3. Create Order as User
    headers = {"Authorization": f"Bearer {user_token}"}
    order_data = {
        "items": [{"product_id": 1, "quantity": 1}]
    }
    res_create = requests.post(f"{BASE_URL}/orders/", json=order_data, headers=headers)
    if res_create.status_code == 200:
        order_id = res_create.json()["id"]
        print(f"✅ Created order #{order_id}")
    else:
        print(f"❌ Failed to create order: {res_create.text}")
        return

    # 4. Fetch Orders as User -> Should see it
    res_list = requests.get(f"{BASE_URL}/orders/", headers=headers)
    orders = res_list.json()
    found = any(o["id"] == order_id for o in orders)
    if found:
        print("✅ User sees their order")
    else:
        print("❌ User cannot see their order!")

    # 5. Admin Check (Optional: Admins should see all)
    admin_token = get_token(ADMIN_CREDS)
    if admin_token:
        res_admin = requests.get(f"{BASE_URL}/orders/", headers={"Authorization": f"Bearer {admin_token}"})
        admin_orders = res_admin.json()
        found_admin = any(o["id"] == order_id for o in admin_orders)
        if found_admin:
            print("✅ Admin sees the order too")
        else:
             print("❌ Admin missed the order")

if __name__ == "__main__":
    test_filtering()
