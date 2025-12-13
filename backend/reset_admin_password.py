import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import SessionLocal
from backend.models import User
from backend.auth import get_password_hash
from sqlalchemy import select

async def reset_admin_password():
    print("🔄 Connecting to database...")
    async with SessionLocal() as db:
        result = await db.execute(select(User).where(User.username == "admin"))
        user = result.scalars().first()
        
        if user:
            print(f"👤 Found user: {user.username}")
            new_password = "admin123"
            user.hashed_password = get_password_hash(new_password)
            await db.commit()
            print(f"✅ Password reset successfully to: {new_password}")
        else:
            print("❌ User 'admin' not found!")
            # Create if not exists (safety net)
            print("creating admin user...")
            admin = User(username="admin", hashed_password=get_password_hash("admin123"), is_admin=True)
            db.add(admin)
            await db.commit()
            print("✅ Admin user created with password: admin123")

if __name__ == "__main__":
    asyncio.run(reset_admin_password())
