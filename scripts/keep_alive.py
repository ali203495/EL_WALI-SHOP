#!/usr/bin/env python3
"""
Keep-Alive Script for Render Backend
Pings the backend API every 10 minutes to prevent it from spinning down.

Usage:
    python keep_alive.py

To run in background (Linux/Mac):
    nohup python keep_alive.py > keep_alive.log 2>&1 &

To stop background process:
    ps aux | grep keep_alive.py
    kill <PID>
"""

import requests
import time
from datetime import datetime

# Configuration
BACKEND_URL = "https://YOUR-BACKEND-URL.onrender.com/"  # Replace with your actual backend URL
PING_INTERVAL = 600  # 10 minutes in seconds (600 seconds)

def ping_backend():
    """Send a GET request to the backend to keep it awake."""
    try:
        response = requests.get(BACKEND_URL, timeout=10)
        
        if response.status_code == 200:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✅ Backend is UP (200 OK)")
        else:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ⚠️  Backend returned {response.status_code}")
            
    except requests.exceptions.Timeout:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ⏱️  Request timed out (backend may be waking up)")
        
    except requests.exceptions.ConnectionError:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ❌ Connection error (backend may be down)")
        
    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ❌ ERROR: {e}")

def main():
    """Main loop to keep pinging the backend."""
    print("=" * 60)
    print("🚀 Keep-Alive Script Started")
    print("=" * 60)
    print(f"🎯 Target: {BACKEND_URL}")
    print(f"⏰ Interval: {PING_INTERVAL // 60} minutes ({PING_INTERVAL} seconds)")
    print(f"📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print("\n⚠️  WARNING: This may violate Render's Terms of Service.")
    print("   For production, consider upgrading to a paid plan.\n")
    print("Press Ctrl+C to stop\n")
    
    try:
        while True:
            ping_backend()
            time.sleep(PING_INTERVAL)
            
    except KeyboardInterrupt:
        print(f"\n\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🛑 Keep-Alive stopped by user")
        print("=" * 60)

if __name__ == "__main__":
    # Check if requests is installed
    try:
        import requests
    except ImportError:
        print("❌ ERROR: 'requests' library not found")
        print("Install it with: pip install requests")
        exit(1)
    
    # Check if URL is configured
    if "YOUR-BACKEND-URL" in BACKEND_URL:
        print("❌ ERROR: Please configure BACKEND_URL in the script")
        print("Edit keep_alive.py and replace YOUR-BACKEND-URL with your actual Render backend URL")
        exit(1)
    
    main()
