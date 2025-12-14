import requests
import sys

BASE_URL = "http://localhost:8000"

def verify_sudo_security():
    print("1. Logging in as Super Admin 'admin'...")
    try:
        resp = requests.post(f"{BASE_URL}/token", data={"username": "admin", "password": "admin123"})
        if resp.status_code != 200:
            print("FAILED: Login")
            return False
        token = resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
    except Exception as e:
        print(f"FAILED: {e}")
        return False

    print("2. Testing /auth/verify-password (Sudo Mode)...")
    # Correct password
    v_resp = requests.post(f"{BASE_URL}/auth/verify-password", json={"password": "admin123"}, headers=headers)
    if v_resp.status_code != 200:
        print(f"FAILED: Verify correct password failed. {v_resp.text}")
        return False
    # Wrong password
    bad_resp = requests.post(f"{BASE_URL}/auth/verify-password", json={"password": "wrong"}, headers=headers)
    if bad_resp.status_code != 400:
        print(f"FAILED: Wrong password accepted? {bad_resp.status_code}")
        return False
    print("   SUCCESS: Password verification works.")

    print("3. Creating Regular Admin...")
    new_user = {
        "username": "regular_admin",
        "password": "password123",
        "email": "reg@example.com",
        "first_name": "Reg",
        "last_name": "Admin",
        "phone_number": "111",
        "is_admin": True,
        "is_super_admin": False
    }
    # Clean up first
    all_users = requests.get(f"{BASE_URL}/users/", headers=headers).json()
    target = next((u for u in all_users if u['username'] == "regular_admin"), None)
    if target:
        requests.delete(f"{BASE_URL}/users/{target['id']}", headers=headers)

    create_resp = requests.post(f"{BASE_URL}/users/", json=new_user, headers=headers)
    if create_resp.status_code != 200:
        print(f"FAILED: Could not create regular admin. {create_resp.text}")
        return False
    
    print("4. Logging in as Regular Admin...")
    reg_resp = requests.post(f"{BASE_URL}/token", data={"username": "regular_admin", "password": "password123"})
    reg_token = reg_resp.json()["access_token"]
    reg_headers = {"Authorization": f"Bearer {reg_token}"}

    print("5. Testing Access Control (Regular Admin should be BLOCKED)...")
    # Try to Read Users
    read_resp = requests.get(f"{BASE_URL}/users/", headers=reg_headers)
    if read_resp.status_code != 403:
        print(f"FAILED: Regular admin could access /users/! Code: {read_resp.status_code}")
        return False
    print("   SUCCESS: /users/ blocked (403).")

    # Try to Create User
    create_try = requests.post(f"{BASE_URL}/users/", json=new_user, headers=reg_headers)
    if create_try.status_code != 403:
         print(f"FAILED: Regular admin could create user! Code: {create_try.status_code}")
         return False
    print("   SUCCESS: create user blocked (403).")

    print("\nOVERALL STATUS: PASS - Sudo Mode and Permissions are secure.")
    return True

if __name__ == "__main__":
    if verify_sudo_security():
        sys.exit(0)
    else:
        sys.exit(1)
