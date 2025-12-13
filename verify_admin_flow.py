import requests
import sqlite3
import time

BASE_URL = "http://localhost:8000"
DB_PATH = "/home/xyz/Documents/xxx/pos.db"

def get_db_token(email):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT reset_token FROM users WHERE email = ?", (email,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def test_admin_flow():
    print("🚀 Starting Verification Flow...")
    
    # 1. Login
    print("1. Logging in as Super Admin...")
    resp = requests.post(f"{BASE_URL}/token", data={"username": "abdelaali", "password": "acbd1234!@#$"})
    if resp.status_code != 200:
        print(f"❌ Login failed: {resp.text}")
        return
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("✅ Logged in.")

    # 2. Create New Admin
    print("2. Creating new admin user 'verify_admin'...")
    new_admin = {
        "username": "verify_admin",
        "password": "initial_password",
        "email": "verify@example.com",
        "first_name": "Verify",
        "last_name": "User",
        "phone_number": "1234567890",
        "is_admin": True
    }
    
    # Delete if exists (cleanup)
    try:
        # Need ID to delete, let's try to get users first
        users = requests.get(f"{BASE_URL}/users/", headers=headers).json()
        for u in users:
            if u['username'] == 'verify_admin':
                 requests.delete(f"{BASE_URL}/users/{u['id']}", headers=headers)
    except:
        pass

    resp = requests.post(f"{BASE_URL}/users/", json=new_admin, headers=headers)
    if resp.status_code != 200:
        print(f"❌ Failed to create admin: {resp.text}")
        return
    print("✅ Admin created.")

    # 3. Forgot Password
    print("3. Requesting password reset...")
    resp = requests.post(f"{BASE_URL}/auth/forgot-password", json={"email": "verify@example.com"})
    if resp.status_code != 200:
        print(f"❌ Failed request: {resp.text}")
        return
    print("✅ Reset request sent.")

    # 4. Get Token manually from DB
    print("4. Fetching reset token from DB...")
    reset_token = get_db_token("verify@example.com")
    if not reset_token:
        print("❌ Reset token not found in DB.")
        return
    print(f"✅ Token found: {reset_token}")

    # 5. Reset Password
    print("5. Resetting password...")
    new_pass = "new_secure_password"
    resp = requests.post(f"{BASE_URL}/auth/reset-password", json={
        "email": "verify@example.com",
        "code": reset_token,
        "new_password": new_pass
    })
    if resp.status_code != 200:
        print(f"❌ Reset failed: {resp.text}")
        return
    print("✅ Password reset successful.")

    # 6. Verify Login with new password
    print("6. Verifying login with new password...")
    resp = requests.post(f"{BASE_URL}/token", data={"username": "verify_admin", "password": new_pass})
    if resp.status_code == 200:
        print("🎉 SUCCESS: Login with new password worked!")
    else:
        print(f"❌ Login with new password failed: {resp.text}")

if __name__ == "__main__":
    test_admin_flow()
