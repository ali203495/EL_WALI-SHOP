import requests
import json

BASE_URL = "http://localhost:8000"

# 1. Login as admin (assuming 'admin' user exists from seed data)
def login(username, password):
    response = requests.post(f"{BASE_URL}/token", data={
        "username": username,
        "password": password
    })
    if response.status_code == 200:
        return response.json()["access_token"]
    return None

# 2. Get Users
def get_users(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/users/", headers=headers)
    if response.status_code == 200:
        return response.json()
    print(f"Failed to get users: {response.text}")
    return []

# 3. Update Password
def update_password(token, user_id, new_password):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.put(
        f"{BASE_URL}/users/{user_id}/password", 
        json={"password": new_password}, 
        headers=headers
    )
    return response.status_code == 200

def main():
    print("Testing Password Update Flow...")
    
    # Prerequisite: Ensure backend is running.
    # We'll assume 'admin' / 'admin123' is the initial credential.
    token = login("admin", "admin")
    if not token:
        print("Initial login failed. User might have changed password already or server not running.")
        # Try finding a way to recover or just fail
        return

    print("Login successful.")
    
    users = get_users(token)
    print(f"Found {len(users)} users.")
    
    if not users:
        print("No users found?")
        return

    target_user = users[0]
    print(f"Targeting user: {target_user['username']} (ID: {target_user['id']})")
    
    new_pass = "abcd1234!@#$"
    if update_password(token, target_user['id'], new_pass):
        print("Password update request successful.")
    else:
        print("Password update failed.")
        return

    # Verify new login
    print("Verifying new login...")
    new_token = login(target_user['username'], new_pass)
    if new_token:
        print("SUCCESS: Login with new password worked!")
        
        # Revert password for safety/convenience if it was admin
        if target_user['username'] == 'admin':
            print("Reverting admin password to 'admin'...")
            update_password(new_token, target_user['id'], "admin")
    else:
        print("FAILURE: Login with new password failed.")

if __name__ == "__main__":
    main()
