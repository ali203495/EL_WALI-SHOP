# Important: Uptime and "Spin Down"

You asked if the site will be **Online 24/24**.

## The Reality of Free Hosting
On **Render's Free Tier**, the server "goes to sleep" (spins down) after 15 minutes of inactivity.
-   **Impact**: The first person to visit the site after a break will wait 30-60 seconds for it to wake up.
-   **Status**: It is technically "online" but slow to start.

## The Solution: "Keep Alive"
To make it **truly 24/24** and fast without paying, you need a service that "pings" your website every 5 minutes to keep it awake.

### Using UptimeRobot (Free)
1.  Go to [uptimerobot.com](https://uptimerobot.com/) and create a free account.
2.  Click **Add New Monitor**.
3.  **Monitor Type**: HTTP(s).
4.  **Friendly Name**: My Website.
5.  **URL**: Enter your Render Backend URL (e.g., `https://maison-api.onrender.com`).
6.  **Monitoring Interval**: 5 minutes (Important!).
7.  Click **Create Monitor**.

Now UptimeRobot will visit your site every 5 minutes, preventing Render from putting it to sleep!
