# 🚀 Quick Deployment Reference

## Fill Out Render Form With These Values:

### Static Site Configuration

**Name:** `maison-frontend` (or your preferred name)

**Branch:** `main` (or your default branch)

**Root Directory:** `frontend`

**Build Command:**
```bash
npm install && npm run generate
```

**Publish Directory:**
```
.output/public
```

### Environment Variables

Click "Advanced" → "Add Environment Variable":

**Key:** `NUXT_PUBLIC_API_BASE`  
**Value:** `https://YOUR-BACKEND-URL.onrender.com/api`

> ⚠️ Replace `YOUR-BACKEND-URL` with your actual backend service URL after deploying the backend first!

---

## Deployment Order

1. **Deploy Backend First** (Web Service)
   - Get the backend URL (e.g., `https://maison-api.onrender.com`)
   
2. **Deploy Frontend** (Static Site)
   - Use the backend URL in the `NUXT_PUBLIC_API_BASE` environment variable

3. **Update Backend CORS**
   - Add frontend URL to `backend/main.py` origins list
   - Commit and push to redeploy

---

## 📖 Full Guide

See [DEPLOYMENT.md](file:///home/xyz/Documents/xxx/DEPLOYMENT.md) for complete step-by-step instructions, troubleshooting, and post-deployment verification.
