import requests
import sys

BASE_URL = "http://localhost:8000"

def verify_final_creds():
    print("Testing 'abdelaali' login...")
    try:
        resp = requests.post(f"{BASE_URL}/token", data={"username": "abdelaali", "password": "abcd1234!@#$"})
        if resp.status_code == 200:
            print("   SUCCESS: abdelaali logged in.")
            if resp.json().get("access_token"):
                 # Check permissions
                 token = resp.json()["access_token"]
                 me = requests.get(f"{BASE_URL}/users/me", headers={"Authorization": f"Bearer {token}"}).json()
                 if me.get("is_super_admin"):
                     print("   SUCCESS: abdelaali is SUper Admin.")
                 else:
                     print("   FAIL: abdelaali is NOT Super Admin.")
                     return False
        else:
            print(f"   FAIL: abdelaali login failed. {resp.status_code}")
            return False

    except Exception as e:
        print(f"Connection error: {e}")
        return False
        
    print("Testing 'admin' login...")
    resp2 = requests.post(f"{BASE_URL}/token", data={"username": "admin", "password": "admin1234"})
    if resp2.status_code == 200:
        print("   SUCCESS: admin logged in.")
        return True
    else:
        print(f"   FAIL: admin login failed. {resp2.status_code}")
        return False

if __name__ == "__main__":
    if verify_final_creds():
        sys.exit(0)
    else:
        sys.exit(1)
