# 🔐 Admin Access & Recovery Guide

## 👑 Default Super Admin Credentials

When the system is first deployed (or the database is reset), a default Super Admin is created automatically:

- **Username**: `admin`
- **Password**: `admin1234`
- **Email**: `admin@example.com`

> [!IMPORTANT]
> You should login immediately and change this password, or create your own personalized admin account.

## 🆘 Recovering a Forgotten Password

Since we have not configured an SMTP (Email) server, password recovery codes are not sent via email. Instead, they are securely logged to the server console.

### How to Reset Your Password

1. **Request Code**: Go to `/forgot-password`, enter your admin email, and click "Send Code".
2. **Find Code**:
   - Go to your **Render Dashboard**.
   - Select the `maison-api` (Backend) service.
   - Click on **"Logs"**.
   - Look for a log line like: `DEBUG: Password reset code for your@email.com: 123456`.
3. **Reset**: Enter that 6-digit code on the website to set a new password.

## 🔄 Emergency Reset

If you are completely locked out and cannot access the logs or the default account:

1. **Redeploy**: In Render, you can manually trigger a redeploy "Clear build cache & deploy".
2. **Database Reset**: Since we are using SQLite on the free tier, redeploying will **RESET the database**.
3. **Login**: You can then login again with the default credentials (`admin` / `admin1234`).

> [!WARNING]
> This "Emergency Reset" will delete all products, orders, and user accounts. Only use this if you are on the free tier and haven't set up a persistent database.
