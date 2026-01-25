import requests
import sys

BASE_URL = "http://localhost:8000"

def test_admin_flow():
    # 1. Login
    print("Trying to login as admin...")
    login_payload = {
        "username": "admin",
        "password": "admin123" # From reset_admin_password.py verification
    }
    
    try:
        response = requests.post(f"{BASE_URL}/token", data=login_payload)
        response.raise_for_status()
        token_data = response.json()
        access_token = token_data["access_token"]
        print("✅ Login successful. Token received.")
    except Exception as e:
        print(f"❌ Login failed: {e}")
        if response:
            print(f"Response: {response.text}")
        sys.exit(1)

    # 2. Get Orders
    print("\nFetching orders as admin...")
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/orders/", headers=headers)
        response.raise_for_status()
        orders = response.json()
        print(f"✅ Orders fetched. Count: {len(orders)}")
        
        if len(orders) > 0:
            print("Latest Order Details:")
            print(orders[-1])
        else:
            print("⚠️ No orders found.")
            
    except Exception as e:
        print(f"❌ Failed to fetch orders: {e}")
        if response:
            print(f"Response: {response.text}")

if __name__ == "__main__":
    test_admin_flow()
