# UptimeRobot Setup - Visual Guide

## Step-by-Step Instructions

### Step 1: Deploy Backend to Render

Before setting up UptimeRobot, you need your backend deployed and running on Render.

**Current Status**: ✅ You're pushing code to GitHub now!

Once your code is pushed:
1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Use these settings:
   - **Name**: `maison-api`
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Click **"Create Web Service"**
6. Wait 5-10 minutes for deployment
7. **Copy your backend URL** (e.g., `https://maison-api.onrender.com`)

---

### Step 2: Sign Up for UptimeRobot

1. Go to https://uptimerobot.com
2. Click **"Register for FREE"**
3. Enter your email and create a password
4. Verify your email
5. Log in to your dashboard

---

### Step 3: Add New Monitor

![UptimeRobot Setup Form](/home/xyz/.gemini/antigravity/brain/89279094-5270-4314-965b-5beb3f5758fc/uptimerobot_setup_guide.png)

In your UptimeRobot dashboard:

1. Click **"+ Add New Monitor"** button
2. Fill in the form:

   | Field | Value |
   |-------|-------|
   | **Monitor Type** | `HTTP(s)` |
   | **Friendly Name** | `Maison API Keep-Alive` |
   | **URL (or IP)** | `https://YOUR-BACKEND-URL.onrender.com/` |
   | **Monitoring Interval** | `Every 5 minutes` |

3. Click **"Create Monitor"**

---

### Step 4: Verify It's Working

After creating the monitor:

1. You'll see your monitor in the dashboard
2. Status should show **"Up"** with a green checkmark ✅
3. UptimeRobot will now ping your backend every 5 minutes
4. Your backend will **never sleep** as long as the monitor is active

---

### Step 5: Optional - Set Up Alerts

Get notified if your backend goes down:

1. Click on your monitor
2. Go to **"Alert Contacts"**
3. Add your email or phone number
4. You'll receive alerts if the backend is unreachable

---

## What Happens Next?

- ✅ UptimeRobot pings your backend every 5 minutes
- ✅ Render keeps your backend awake (no cold starts)
- ✅ Your users get instant API responses
- ✅ You get alerts if something goes wrong

---

## Important Notes

> [!WARNING]
> **Terms of Service**: Using keep-alive services technically violates Render's free tier ToS. They may suspend your account if detected. For production sites, upgrade to the paid plan ($7/month).

> [!TIP]
> **Free Tier Limits**: UptimeRobot's free tier allows 50 monitors with 5-minute intervals. More than enough for your needs!

> [!NOTE]
> **Frontend**: Your static site frontend doesn't need this - it's always available instantly!

---

## Troubleshooting

### Monitor shows "Down"
- Check if your backend is deployed and running on Render
- Verify the URL is correct (should end with `/`)
- Wait a few minutes - backend might be doing initial deployment

### Backend still has cold starts
- Check UptimeRobot monitor is active (green checkmark)
- Verify interval is set to 5 minutes (not longer)
- Check UptimeRobot logs to see if pings are successful

### Account suspended by Render
- This means Render detected the keep-alive pings
- Upgrade to paid plan ($7/month) to avoid this
- Or migrate to Railway/Fly.io with better free tiers

---

## Cost Comparison

| Solution | Cost | Setup Time | Reliability |
|----------|------|------------|-------------|
| **UptimeRobot (Free)** | $0 | 5 min | Medium |
| **Render Paid Plan** | $7/mo | 2 min | High ✅ |

**Recommendation**: Use UptimeRobot for testing/development, upgrade to paid for production.

---

## Next Steps

1. ✅ Push code to GitHub (you're doing this now!)
2. ⏳ Deploy backend to Render
3. ⏳ Get backend URL
4. ⏳ Set up UptimeRobot monitor
5. ⏳ Deploy frontend static site
6. ✅ Your site is live 24/7!

---

**Need help?** Check [DEPLOYMENT.md](file:///home/xyz/Documents/xxx/DEPLOYMENT.md) for full deployment guide.
