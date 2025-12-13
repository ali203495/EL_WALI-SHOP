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
    return None

def main():
    color_print("Testing Super Admin Privileges...", "yellow")

    # 1. Login as Super Admin
    admin_token = login(ADMIN_USER, ADMIN_PASS)
    if not admin_token:
        color_print("Failed to login as admin", "red")
        sys.exit(1)
    color_print(f"Logged in as {ADMIN_USER}", "green")

    # 2. Create Sub-Admin User
    headers = {"Authorization": f"Bearer {admin_token}"}
    sub_admin = {
        "username": "subadmin",
        "password": "subpassword",
        "is_admin": True
    }
    
    # Try creating (or getting if exists)
    try:
        r = requests.post(f"{BASE_URL}/users/", json=sub_admin, headers=headers)
        if r.status_code == 200:
             sub_admin_id = r.json()["id"]
             color_print(f"Created sub-admin (ID: {sub_admin_id})", "green")
        elif r.status_code == 400 and "registered" in r.text:
             color_print("Sub-admin already exists, getting ID...", "yellow")
             users = requests.get(f"{BASE_URL}/users/", headers=headers).json()
             for u in users:
                 if u["username"] == "subadmin":
                     sub_admin_id = u["id"]
                     break
    except Exception as e:
        color_print(f"Error creating/finding subadmin: {e}", "red")
        sys.exit(1)

    # 3. Login as Sub-Admin
    sub_token = login("subadmin", "subpassword")
    if not sub_token:
        color_print("Failed to login as subadmin", "red")
        sys.exit(1)
    color_print("Logged in as subadmin", "green")
    
    sub_headers = {"Authorization": f"Bearer {sub_token}"}

    # 4. Try to Create User (Should Fail)
    color_print("Attempting to create user as subadmin (Should Fail)...", "yellow")
    r = requests.post(f"{BASE_URL}/users/", json={"username": "testuser", "password": "pw"}, headers=sub_headers)
    if r.status_code == 403:
        color_print("SUCCESS: Sub-admin denied creation rights.", "green")
    else:
        color_print(f"FAILURE: Sub-admin response code: {r.status_code}", "red")

    # 5. Try to Change Admin Password (Should Fail)
    color_print("Attempting to change admin password as subadmin (Should Fail)...", "yellow")
    # need admin id, assume 1
    r = requests.put(f"{BASE_URL}/users/1/password", json={"password": "hacked"}, headers=sub_headers)
    if r.status_code == 403:
        color_print("SUCCESS: Sub-admin denied password change rights.", "green")
    else:
        color_print(f"FAILURE: Sub-admin response code: {r.status_code}", "red")

    # 6. Delete Sub-Admin (clean up) as Admin
    color_print("Cleaning up: Deleting subadmin as Admin...", "yellow")
    r = requests.delete(f"{BASE_URL}/users/{sub_admin_id}", headers=headers)
    if r.status_code == 200:
        color_print("SUCCESS: Admin deleted user.", "green")
    else:
        color_print(f"FAILURE: Admin failed to delete user: {r.status_code}", "red")

if __name__ == "__main__":
    main()
