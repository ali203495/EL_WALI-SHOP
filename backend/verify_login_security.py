import requests
import sys

BASE_URL = "http://localhost:8000"

def verify_full_login_security():
    print("1. Creating regular admin and super admin...")
    # Assume 'admin' exists. Create 'reg_admin'
    admin_token = requests.post(f"{BASE_URL}/token", data={"username": "admin", "password": "admin123"}).json()["access_token"]
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    reg_user = {
        "username": "reg_login_test", "password": "password123", "email": "reglogin@ex.com", 
        "first_name": "R", "last_name": "A", "phone_number": "222", "is_admin": True, "is_super_admin": False
    }
    # Cleanup
    users = requests.get(f"{BASE_URL}/users/", headers=headers).json()
    target = next((u for u in users if u['username'] == "reg_login_test"), None)
    if target: requests.delete(f"{BASE_URL}/users/{target['id']}", headers=headers)
    
    requests.post(f"{BASE_URL}/users/", json=reg_user, headers=headers)
    
    print("2. Login as regular admin...")
    reg_token = requests.post(f"{BASE_URL}/token", data={"username": "reg_login_test", "password": "password123"}).json()["access_token"]
    reg_headers = {"Authorization": f"Bearer {reg_token}"}
    
    print("3. Verify Super Credentials Endpoint...")
    # Case A: Correct Super Admin Creds
    valid_super = requests.post(f"{BASE_URL}/auth/verify-super-credentials", 
                                json={"username": "admin", "password": "admin123"}, headers=reg_headers)
    if valid_super.status_code == 200 and valid_super.json().get("is_super_admin"):
        print("   headers: Valid Super Admin credentials verified successfully.")
    else:
        print(f"FAILED: Valid super admin creds rejected. {valid_super.text}")
        return False
        
    # Case B: Correct Regular Admin Creds (Should fail is_super_admin check)
    valid_reg = requests.post(f"{BASE_URL}/auth/verify-super-credentials", 
                              json={"username": "reg_login_test", "password": "password123"}, headers=reg_headers)
    if valid_reg.status_code == 403:
        print("   SUCCESS: Regular admin credentials rejected (403).")
    else:
        print(f"FAILED: Regular admin creds accepted? {valid_reg.status_code} {valid_reg.text}")
        return False

    # Case C: Wrong Password
    wrong = requests.post(f"{BASE_URL}/auth/verify-super-credentials", 
                          json={"username": "admin", "password": "wrongpassword"}, headers=reg_headers)
    if wrong.status_code == 400:
        print("   SUCCESS: Wrong password rejected (400).")
    else:
        print(f"FAILED: Wrong password accepted? {wrong.status_code}")
        return False
        
    print("\nOVERALL STATUS: PASS - Full Login Protection Working.")
    return True

if __name__ == "__main__":
    if verify_full_login_security():
        sys.exit(0)
    else:
        sys.exit(1)
