# Deployment & Domain Guide

## 1. Buying a Domain
To make your site professional (e.g., `www.maisonelwali.com`), you need to buy a domain.

**Recommended Registrars:**
-   **Namecheap**: Affordable, great support.
-   **GoDaddy**: Popular, good introductory offers.
-   **Porkbun**: Very transparent pricing, no hidden fees.

**Steps:**
1.  Go to one of the sites above.
2.  Search for "maisonelwali".
3.  Choose an extension (preferably `.com` for luxury brands, or `.ae` if strictly local to UAE).
4.  Purchase it (usually $10-15/year).

---

## 2. Hosting Your Application
Your app has two parts: Backend (Python) and Frontend (Nuxt).

### Option A: Render.com (Recommended - Easiest)
Render can host both your backend and frontend easily.
1.  **Sign up** at dashboard.render.com.
2.  **Connect GitHub**: You need to push your code to GitHub first.
3.  **Backend Service**:
    -   Create "Web Service".
    -   Connect your repo.
    -   Root Directory: `backend`.
    -   Build Command: `pip install -r requirements.txt`.
    -   Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`.
    -   Add Environment Variables from your `.env` (Database URL, Facebook Token, etc.).
4.  **Frontend Service**:
    -   Create "Static Site" (if using `nuxt generate`) or "Web Service" (Node) if using SSR.
    -   Root Directory: `frontend`.
    -   Build Command: `npm install && npm run build`.
    -   Start Command: `npm run preview` (or `node .output/server/index.mjs`).
    -   Add Environment Variable: `NUXT_PUBLIC_API_BASE` pointing to your Backend URL.

### Option B: Vercel (Frontend) + Railway (Backend)
-   **Vercel** is optimized for Nuxt. Just import your repo, it detects Nuxt automatically.
-   **Railway** is great for Python/Databases.

---

## 3. Connecting Domain
Once hosted:
1.  Go to your Host's settings (e.g., Render > Settings > Custom Domains).
2.  Enter your new domain (`maisonelwali.com`).
3.  It will give you DNS records (A Record or CNAME).
4.  Go to your Domain Registrar (Namecheap/GoDaddy) > DNS Settings.
5.  Add the records provided by the host.

## Recommended Next Steps
1.  Push your code to **GitHub**.
2.  Create an account on **Render.com**.
3.  Follow the setup above!
