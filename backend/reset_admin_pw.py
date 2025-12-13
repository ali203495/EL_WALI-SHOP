import asyncio
import sys
import os

from database import SessionLocal
from models import User
from auth import get_password_hash
from sqlalchemy import select

async def reset_admin():
    username = "admin"
    new_password = "admin123" # Temporary safe default to communicate to user
    
    print(f"🔄 Resetting password for user: {username}")
    
    async with SessionLocal() as db:
        result = await db.execute(select(User).where(User.username == username))
        user = result.scalars().first()
        
        if not user:
            print("❌ Admin user not found. Creating one...")
            user = User(
                username=username,
                hashed_password=get_password_hash(new_password),
                is_admin=True,
                is_active=True
            )
            db.add(user)
        else:
            print("✅ Admin user found. Updating password...")
            user.hashed_password = get_password_hash(new_password)
            user.is_admin = True
            user.is_active = True
            
        await db.commit()
        print(f"✨ Success! Password set to: {new_password}")

if __name__ == "__main__":
    asyncio.run(reset_admin())
