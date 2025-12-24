
import asyncio
import httpx
import os
import sys

# Color codes
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

BASE_URL = "http://localhost:8000"

async def verify_health(client):
    print("1. Verifying API Health...")
    try:
        resp = await client.get(f"{BASE_URL}/")
        if resp.status_code == 200:
            print(f"{GREEN}✓ API is reachable.{RESET}")
        else:
            print(f"{RED}✗ API returned {resp.status_code}{RESET}")
            return False
    except Exception as e:
        print(f"{RED}✗ Connection failed: {e}{RESET}")
        return False
    return True

async def verify_settings(client):
    print("\n2. Verifying Site Settings URL...")
    try:
        resp = await client.get(f"{BASE_URL}/settings/")
        if resp.status_code == 200:
            data = resp.json()
            print(f"{GREEN}✓ Settings endpoint active. Found {len(data)} settings.{RESET}")
        else:
            print(f"{RED}✗ Settings endpoint failed: {resp.status_code}{RESET}")
    except Exception as e:
        print(f"{RED}✗ Settings check failed: {e}{RESET}")

async def verify_facebook_config():
    print("\n3. Verifying Facebook Configuration...")
    # Manual check of .env or env vars
    # We can't easily check loaded env vars of the running server from outside without an endpoint,
    # but we can check the local .env file.
    
    has_token = False
    try:
        with open(".env", "r") as f:
            content = f.read()
            if "FACEBOOK_ACCESS_TOKEN" in content and "EAA" in content:
                has_token = True
    except:
        pass

    if has_token:
        print(f"{GREEN}✓ FACEBOOK_ACCESS_TOKEN found in .env.{RESET}")
    else:
        print(f"{RED}⚠ FACEBOOK_ACCESS_TOKEN missing or invalid in .env.{RESET}")
        print(f"  {RED}Auto-posting will be SKIPPED (Safe Mode).{RESET}")

async def main():
    print("--- STARTING SYSTEM VERIFICATION ---\n")
    
    async with httpx.AsyncClient() as client:
        if not await verify_health(client):
            print("\nAborting: System is down.")
            return

        await verify_settings(client)
        
        # Facebook check
        await verify_facebook_config()
        
    print("\n--- VERIFICATION COMPLETE ---")

if __name__ == "__main__":
    # Ensure we are in backend dir
    if not os.path.exists("main.py"):
        print("Error: Please run this from the backend directory.")
        sys.exit(1)
        
    asyncio.run(main())
