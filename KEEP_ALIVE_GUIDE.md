# Keep Your Website Running 24/7

## The Problem

On Render's **free tier**, web services automatically **spin down after 15 minutes of inactivity**. When a request comes in, the service "wakes up" (cold start), which can take 30-60 seconds.

**Static sites don't have this problem** - your frontend will always be available instantly. Only the **backend API** spins down.

## Solutions (Ranked by Cost)

### 🆓 Option 1: Free Keep-Alive Service (Recommended for Testing)

Use a free service to ping your backend every 10-14 minutes to keep it awake.

#### Services You Can Use:
- **UptimeRobot** (https://uptimerobot.com) - Free, 50 monitors
- **Cron-Job.org** (https://cron-job.org) - Free, unlimited jobs
- **BetterUptime** (https://betteruptime.com) - Free tier available

#### Setup with UptimeRobot:

1. **Sign up** at https://uptimerobot.com (free)
2. **Add New Monitor**:
   - Monitor Type: `HTTP(s)`
   - Friendly Name: `Maison API Keep-Alive`
   - URL: `https://YOUR-BACKEND-URL.onrender.com/`
   - Monitoring Interval: `5 minutes` (or shortest available)
3. **Save** - Your backend will now be pinged every 5 minutes

#### Pros:
- ✅ Completely free
- ✅ Easy to set up (5 minutes)
- ✅ Also monitors if your site goes down

#### Cons:
- ❌ Still violates Render's Terms of Service (they discourage this)
- ❌ May still have occasional cold starts
- ❌ Render may suspend your account if detected

---

### 💰 Option 2: Upgrade to Render Paid Plan (Best Solution)

**Cost**: $7/month per service

Upgrade your backend to a paid instance type.

#### Benefits:
- ✅ **Never spins down** - always running
- ✅ **Better performance** - more CPU/RAM
- ✅ **Persistent disk** - SQLite data won't be lost
- ✅ **Compliant** with Render's terms
- ✅ **Professional** - suitable for production

#### How to Upgrade:

1. Go to your backend service in Render dashboard
2. Click **"Settings"**
3. Scroll to **"Instance Type"**
4. Select **"Starter"** ($7/month) or higher
5. Click **"Save Changes"**

**Total Cost**: $7/month (frontend static site remains free)

---

### 🔄 Option 3: Self-Hosted Keep-Alive Script

Run a script on your local machine or a VPS to ping your backend.

#### Create `keep_alive.py`:

```python
import requests
import time
from datetime import datetime

BACKEND_URL = "https://YOUR-BACKEND-URL.onrender.com/"
PING_INTERVAL = 600  # 10 minutes in seconds

def ping_backend():
    try:
        response = requests.get(BACKEND_URL, timeout=10)
        status = "✅ UP" if response.status_code == 200 else f"⚠️ {response.status_code}"
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {status}")
    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ❌ ERROR: {e}")

if __name__ == "__main__":
    print(f"🚀 Keep-Alive started for {BACKEND_URL}")
    print(f"⏰ Pinging every {PING_INTERVAL // 60} minutes\n")
    
    while True:
        ping_backend()
        time.sleep(PING_INTERVAL)
```

#### Run it:

```bash
# Install requests if needed
pip install requests

# Run the script (keep terminal open)
python keep_alive.py
```

#### Run in Background (Linux/Mac):

```bash
nohup python keep_alive.py > keep_alive.log 2>&1 &
```

#### Pros:
- ✅ Free if you have a computer/server running 24/7
- ✅ Full control

#### Cons:
- ❌ Requires a machine running 24/7
- ❌ Still violates Render's ToS
- ❌ Not reliable if your machine goes offline

---

### 🌐 Option 4: Deploy to Alternative Platforms

Consider platforms with better free tiers:

#### **Railway** (https://railway.app)
- **Free tier**: $5 credit/month (usually enough for small apps)
- **No sleep** on free tier
- **Pros**: Similar to Render, easy deployment
- **Cons**: Limited free credit

#### **Fly.io** (https://fly.io)
- **Free tier**: 3 shared VMs, 160GB bandwidth
- **No sleep** on free tier
- **Pros**: Better free tier, global deployment
- **Cons**: Slightly more complex setup

#### **Vercel** (Frontend) + **Railway/Fly** (Backend)
- **Vercel**: Free unlimited static hosting
- **Railway/Fly**: Backend API
- **Pros**: Best performance, no sleep
- **Cons**: Need to manage two platforms

---

### 🏢 Option 5: VPS Hosting (Most Control)

Deploy to a VPS for full control.

#### Providers:
- **DigitalOcean**: $4-6/month
- **Linode**: $5/month
- **Vultr**: $2.50-6/month
- **Hetzner**: €4.50/month (~$5)

#### Pros:
- ✅ Full control
- ✅ Always running
- ✅ Can host both frontend and backend
- ✅ Better for scaling

#### Cons:
- ❌ Requires server management skills
- ❌ Need to set up deployment, SSL, etc.
- ❌ More complex

---

## My Recommendation

### For Development/Testing:
**Use UptimeRobot** (free keep-alive service) - Quick and easy, but not for long-term production.

### For Production (Real Users):
**Upgrade to Render Paid Plan** ($7/month) - Most reliable, compliant, and professional solution.

### For Budget-Conscious Production:
**Fly.io or Railway** - Better free tiers without sleep, but may require migration.

---

## Implementation: UptimeRobot Setup (Fastest)

Since you're already on Render, here's the quickest solution:

1. **Deploy your backend** to Render (if not already done)
2. **Get the backend URL** (e.g., `https://maison-api.onrender.com`)
3. **Sign up** at https://uptimerobot.com
4. **Add Monitor**:
   - URL: `https://maison-api.onrender.com/`
   - Interval: `5 minutes`
5. **Done!** Your backend will stay awake

**Note**: This is against Render's ToS, so use at your own risk. For production, upgrade to paid.

---

## Implementation: Upgrade to Paid (Recommended)

1. Go to https://dashboard.render.com
2. Select your backend service (`maison-api`)
3. Click **Settings** → **Instance Type**
4. Select **Starter ($7/month)**
5. Click **Save Changes**
6. **Done!** Your backend will never sleep

---

## Cost Comparison

| Solution | Monthly Cost | Reliability | Compliant | Setup Time |
|----------|-------------|-------------|-----------|------------|
| UptimeRobot | $0 | Medium | ❌ No | 5 min |
| Render Paid | $7 | High | ✅ Yes | 2 min |
| Railway | $0-5 | High | ✅ Yes | 15 min |
| Fly.io | $0 | High | ✅ Yes | 20 min |
| VPS | $4-6 | High | ✅ Yes | 1-2 hours |

---

## What About the Frontend?

**Good news**: Your frontend (static site) **never goes down** on Render! Static sites are always available with instant loading.

Only the **backend API** has the sleep issue.

---

## Questions?

- **"Will my frontend go down?"** - No, only the backend API sleeps.
- **"How long is cold start?"** - Usually 30-60 seconds for the first request.
- **"Can I use multiple keep-alive services?"** - Yes, but it's still against ToS.
- **"Is $7/month worth it?"** - Yes, for a production site with real users.

---

**Recommendation**: Start with UptimeRobot for testing, then upgrade to Render Paid ($7/month) when you're ready for production.
