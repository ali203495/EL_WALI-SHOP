import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import SessionLocal
from backend.models import User
from backend.auth import get_password_hash
from sqlalchemy import select

async def update_super_admin():
    print("🔄 Connecting to database...")
    async with SessionLocal() as db:
        target_username = "Abdelaali"
        target_email = "abdelaali.markabi@gmail.com"
        target_password = "abcd1234!@#$%"
        
        # Check if user exists (case insensitive check for safety, but we want exact casing)
        # We'll look for "Abdelaali" or "abdelaali" and unify/update.
        
        result = await db.execute(select(User).where(User.username.in_(["Abdelaali", "abdelaali"])))
        user = result.scalars().first()
        
        if user:
            print(f"👤 Found existing user: {user.username}")
            user.username = target_username
            user.email = target_email
            user.hashed_password = get_password_hash(target_password)
            user.is_admin = True
            await db.commit()
            print(f"✅ Updated super admin: {user.username}")
        else:
            print(f"➕ Creating new super admin: {target_username}")
            new_user = User(
                username=target_username,
                email=target_email,
                hashed_password=get_password_hash(target_password),
                is_admin=True,
                first_name="Abdelaali",
                last_name="Admin"
            )
            db.add(new_user)
            await db.commit()
            print("✅ Super admin created successfully")

if __name__ == "__main__":
    asyncio.run(update_super_admin())
