# Maison El Wali - Render Deployment Guide

This guide walks you through deploying the Maison El Wali application to Render with both backend API and frontend static site.

## 📋 Prerequisites

- GitHub repository with your code pushed
- Render account (free tier available at [render.com](https://render.com))
- Both backend and frontend code in the same repository

## 🚀 Deployment Steps

### Step 1: Deploy Backend API (Web Service)

1. **Go to Render Dashboard** → Click **"New +"** → Select **"Web Service"**

2. **Connect Repository**: 
   - Connect your GitHub account
   - Select your repository (`ali203495/r_` or your repo name)

3. **Configure Backend Service**:
   ```
   Name:                maison-api
   Region:              Choose closest to your users
   Branch:              main (or your default branch)
   Root Directory:      backend
   Runtime:             Python 3
   Build Command:       pip install -r requirements.txt
   Start Command:       uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

4. **Environment Variables** (click "Advanced" → "Add Environment Variable"):
   ```
   PYTHON_VERSION = 3.11
   ```

5. **Instance Type**: Free (or paid if needed)

6. **Click "Create Web Service"**

7. **Wait for deployment** (5-10 minutes). Once deployed, note the URL (e.g., `https://maison-api.onrender.com`)

> [!IMPORTANT]
> **Database Persistence**: The backend uses SQLite which stores data in `pos.db`. On Render's free tier, this file will be lost on each deploy. For production, consider:
> - Upgrading to a paid plan with persistent disk storage
> - Migrating to PostgreSQL (Render offers free PostgreSQL databases)

### Step 2: Deploy Frontend (Static Site)

1. **Go to Render Dashboard** → Click **"New +"** → Select **"Static Site"**

2. **Connect Repository**: Select the same repository

3. **Configure Static Site** (THIS IS WHAT YOU'RE FILLING OUT NOW):
   ```
   Name:                maison-frontend
   Branch:              main
   Root Directory:      frontend
   Build Command:       npm install && npm run generate
   Publish Directory:   .output/public
   ```

4. **Environment Variables** (click "Advanced" → "Add Environment Variable"):
   ```
   Key:   NUXT_PUBLIC_API_BASE
   Value: https://maison-api.onrender.com/api
   ```
   
   > Replace `https://maison-api.onrender.com` with your actual backend URL from Step 1

5. **Auto-Deploy**: Yes (recommended - deploys on git push)

6. **Click "Create Static Site"**

7. **Wait for deployment** (3-5 minutes)

### Step 3: Update Backend CORS Settings

After deployment, you need to update the backend to allow requests from your frontend domain.

1. **Edit** `backend/main.py` (lines 45-52)
2. **Add your frontend URL** to the `origins` list:
   ```python
   origins = [
       "http://localhost:3000",
       "http://127.0.0.1:3000",
       "https://maison-frontend.onrender.com",  # Add this
       # Add custom domain if you have one
   ]
   ```

3. **Commit and push** to trigger auto-deploy:
   ```bash
   git add backend/main.py
   git commit -m "Add production frontend URL to CORS"
   git push
   ```

## ✅ Post-Deployment Verification

### 1. Test Backend API

Visit your backend URL in a browser:
```
https://maison-api.onrender.com/
```

You should see:
```json
{"message": "POS & Admin API is running"}
```

### 2. Test Frontend

Visit your frontend URL:
```
https://maison-frontend.onrender.com/
```

The site should load with the full Maison El Wali interface.

### 3. Test Admin Login

1. Go to `https://maison-frontend.onrender.com/admin`
2. Login with:
   - **Username**: `abdelaali`
   - **Password**: `Abdelaali@2024`

### 4. Test API Integration

- Navigate through the catalog
- Try adding items to cart
- Check if product data loads correctly

## 🔧 Configuration Files Reference

### Current `render.yaml`

Your repository includes a `render.yaml` file that can automate deployment, but since you're using the web UI, you can ignore it or update it to match your manual configuration.

### Environment Variables Summary

**Backend (`maison-api`)**:
- `PYTHON_VERSION`: `3.11`

**Frontend (`maison-frontend`)**:
- `NUXT_PUBLIC_API_BASE`: `https://maison-api.onrender.com/api` (your backend URL + `/api`)

## 🌐 Custom Domain (Optional)

### For Static Site (Frontend):
1. Go to your static site settings in Render
2. Click "Custom Domains"
3. Add your domain (e.g., `www.maisonelwali.com`)
4. Follow DNS configuration instructions

### For Web Service (Backend):
1. Go to your web service settings
2. Click "Custom Domains"
3. Add API subdomain (e.g., `api.maisonelwali.com`)

## 🐛 Troubleshooting

### Frontend shows "Failed to fetch" errors

**Cause**: Frontend can't reach backend API

**Solutions**:
1. Verify `NUXT_PUBLIC_API_BASE` environment variable is set correctly
2. Check backend CORS settings include frontend URL
3. Ensure backend service is running (check Render dashboard)

### Backend shows "Application failed to start"

**Cause**: Missing dependencies or configuration error

**Solutions**:
1. Check build logs in Render dashboard
2. Verify `requirements.txt` includes all dependencies
3. Ensure `uvicorn` is in `requirements.txt`

### Database is empty after deployment

**Cause**: SQLite database is not persistent on free tier

**Solutions**:
1. Upgrade to paid tier with persistent disk
2. Migrate to PostgreSQL:
   - Create PostgreSQL database in Render
   - Update `database.py` to use PostgreSQL connection
   - Add `psycopg2-binary` to `requirements.txt`

### Static site build fails

**Cause**: Build command or publish directory incorrect

**Solutions**:
1. Verify build command: `npm install && npm run generate`
2. Verify publish directory: `.output/public`
3. Check build logs for specific errors

### Images/uploads not showing

**Cause**: Static files are stored locally in backend, not accessible after deployment

**Solutions**:
1. Use cloud storage (AWS S3, Cloudinary, etc.) for uploads
2. Update upload endpoint to use cloud storage service

## 📊 Free Tier Limitations

**Render Free Tier includes**:
- ✅ 750 hours/month of runtime
- ✅ Automatic HTTPS
- ✅ Continuous deployment from Git
- ❌ Services spin down after 15 minutes of inactivity (cold starts)
- ❌ No persistent disk storage (SQLite data lost on redeploy)

**Recommendations**:
- For production, upgrade to paid tier ($7/month per service)
- Use PostgreSQL for database persistence
- Consider cloud storage for uploaded images

## 🎯 Next Steps

1. ✅ Deploy backend and frontend
2. ✅ Test all functionality
3. 🔄 Set up PostgreSQL database (recommended)
4. 🔄 Configure cloud storage for uploads
5. 🔄 Add custom domain
6. 🔄 Set up monitoring and alerts

## 📞 Support

- **Render Docs**: https://render.com/docs
- **Nuxt Deployment**: https://nuxt.com/docs/getting-started/deployment
- **FastAPI Deployment**: https://fastapi.tiangolo.com/deployment/

---

**Deployed by**: Antigravity AI Assistant  
**Last Updated**: 2025-12-14
