# How to Upload Your Code

You are one step away! Your code is saved on your computer, but you need to send it to the cloud.

## Step 1: Create a GitHub Repository
1.  Go to [github.com/new](https://github.com/new).
2.  Name it `maison-el-wali`.
3.  Click **Create repository**.

## Step 2: Push Your Code
Copy the **HTTPS URL** of your new repository (it looks like `https://github.com/YourName/maison-el-wali.git`).

Then, run these commands in your terminal:

```bash
# 1. Remove the old (broken) link
git remote remove origin

# 2. Add your new link (REPLACE THE URL!)
git remote add origin https://github.com/YOUR_USERNAME/maison-el-wali.git

# 3. Upload everything
git branch -M main
git push -u origin main
```

## Step 3: Deploy
Once the code is on GitHub, go to **Render.com** and connect this repository (as explained in `DEPLOYMENT_GUIDE.md`).
