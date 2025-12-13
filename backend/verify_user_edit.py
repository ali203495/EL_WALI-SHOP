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
    color_print("Testing Full User Edit Privileges...", "yellow")

    # 1. Login as Super Admin (abdelaali)
    admin_token = login(ADMIN_USER, ADMIN_PASS)
    if not admin_token:
        color_print("Failed to login as super admin", "red")
        sys.exit(1)
    color_print(f"Logged in as {ADMIN_USER}", "green")

    headers = {"Authorization": f"Bearer {admin_token}"}

    # 2. Create Test User
    test_user = {"username": "to_be_edited", "password": "pw", "is_admin": False}
    r = requests.post(f"{BASE_URL}/users/", json=test_user, headers=headers)
    if r.status_code == 200:
        user_id = r.json()["id"]
        color_print(f"Created test user (ID: {user_id})", "green")
    else:
        # User might exist, find him
        users = requests.get(f"{BASE_URL}/users/", headers=headers).json()
        for u in users:
            if u["username"] == "to_be_edited":
                user_id = u["id"]
                break
        else:
            color_print("Could not create or find test user", "red")
            sys.exit(1)

    # 3. Update User (Super Admin)
    color_print("Updating user: Renaming to 'edited_user' and making Admin...", "yellow")
    update_data = {
        "username": "edited_user",
        "is_admin": True,
        "is_active": True
    }
    r = requests.put(f"{BASE_URL}/users/{user_id}", json=update_data, headers=headers)
    if r.status_code == 200:
        updated = r.json()
        if updated["username"] == "edited_user" and updated["is_admin"] is True:
            color_print("SUCCESS: User updated successfully by Super Admin.", "green")
        else:
            color_print(f"FAILURE: User update mismatch: {updated}", "red")
    else:
        color_print(f"FAILURE: Update failed with {r.status_code}", "red")

    # 4. Create Sub Admin to test restriction
    sub_admin = {"username": "sub_editor", "password": "pw", "is_admin": True}
    r = requests.post(f"{BASE_URL}/users/", json=sub_admin, headers=headers)
    sub_id = r.json()["id"] if r.status_code == 200 else None
    
    # Login as Sub Admin
    sub_token = login("sub_editor", "pw")
    if sub_token:
        color_print("Logged in as Sub Admin", "green")
        sub_headers = {"Authorization": f"Bearer {sub_token}"}
        
        # Try to update the user (should fail)
        color_print("Attempting update as Sub Admin (Should Fail)...", "yellow")
        r = requests.put(f"{BASE_URL}/users/{user_id}", json={"username": "hacked_user"}, headers=sub_headers)
        if r.status_code == 403:
            color_print("SUCCESS: Sub Admin denied update rights.", "green")
        else:
            color_print(f"FAILURE: Sub Admin got code {r.status_code}", "red")

    # 5. Cleanup
    color_print("Cleaning up...", "yellow")
    requests.delete(f"{BASE_URL}/users/{user_id}", headers=headers)
    if sub_id:
        requests.delete(f"{BASE_URL}/users/{sub_id}", headers=headers)

if __name__ == "__main__":
    main()
