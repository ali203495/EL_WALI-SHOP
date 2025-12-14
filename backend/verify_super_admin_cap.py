import requests
import sys

BASE_URL = "http://localhost:8000"

def verify_admin_capabilities():
    print("1. Logging in as 'admin'...")
    try:
        resp = requests.post(f"{BASE_URL}/token", data={"username": "admin", "password": "admin123"})
        if resp.status_code != 200:
            print(f"FAILED: Could not login as admin. {resp.status_code} {resp.text}")
            return False
        token = resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print("   SUCCESS: Logged in.")
    except Exception as e:
        print(f"FAILED: Connection error. {e}")
        return False

    print("2. Checking 'admin' details...")
    resp = requests.get(f"{BASE_URL}/users/me", headers=headers)
    user_data = resp.json()
    if not user_data.get("is_admin"):
        print(f"FAILED: 'admin' user does not have is_admin=True. Data: {user_data}")
        return False
    print("   SUCCESS: 'admin' has is_admin=True.")

    print("3. Attempting to create a test admin user...")
    new_user = {
        "username": "test_admin_99",
        "password": "password123",
        "email": "test99@example.com",
        "first_name": "Test",
        "last_name": "Admin",
        "phone_number": "123456",
        "is_admin": True
    }
    # First delete if exists from previous run (cleanup)
    requests.delete(f"{BASE_URL}/users/9999", headers=headers) # ID won't match, simplistic cleanup usually needs lookup

    resp = requests.post(f"{BASE_URL}/users/", json=new_user, headers=headers)
    if resp.status_code == 200:
        created_user = resp.json()
        print(f"   SUCCESS: Created user {created_user['username']} (ID: {created_user['id']})")
        
        print("4. Attempting to delete the test user...")
        del_resp = requests.delete(f"{BASE_URL}/users/{created_user['id']}", headers=headers)
        if del_resp.status_code == 200:
            print("   SUCCESS: Deleted test user.")
            return True
        else:
            print(f"FAILED: Could not delete user. {del_resp.status_code} {del_resp.text}")
            return False
    else:
        if "already registered" in resp.text:
             print("   User exists, trying to delete specific username lookup...")
             # Retrieve all users to find ID
             all_users = requests.get(f"{BASE_URL}/users/", headers=headers).json()
             target = next((u for u in all_users if u['username'] == "test_admin_99"), None)
             if target:
                 del_resp = requests.delete(f"{BASE_URL}/users/{target['id']}", headers=headers)
                 if del_resp.status_code == 200:
                     print("   SUCCESS: Deleted existing test user.")
                     return True
        print(f"FAILED: Could not create user. {resp.status_code} {resp.text}")
        return False

if __name__ == "__main__":
    if verify_admin_capabilities():
        print("\nOVERALL STATUS: PASS - 'admin' is a fully functional Super Admin.")
        sys.exit(0)
    else:
        print("\nOVERALL STATUS: FAIL")
        sys.exit(1)
