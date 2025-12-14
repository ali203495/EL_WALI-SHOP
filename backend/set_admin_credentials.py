import asyncio
from database import async_session
from models import User
from auth import get_password_hash
from sqlalchemy import select

async def set_admin_credentials():
    async with async_session() as db:
        print("Checking for 'admin' user...")
        result = await db.execute(select(User).where(User.username == "admin"))
        user = result.scalars().first()
        
        hashed_pwd = get_password_hash("admin123")
        
        if user:
            print("User 'admin' found. Updating password and permissions...")
            user.hashed_password = hashed_pwd
            user.is_admin = True
            user.is_super_admin = True
            user.is_active = True
        else:
            print("User 'admin' not found. Creating new super admin...")
            user = User(
                username="admin",
                hashed_password=hashed_pwd,
                email="admin@example.com",
                first_name="Super",
                last_name="Admin",
                phone_number="0000000000",
                is_admin=True,
                is_super_admin=True,
                is_active=True
            )
            db.add(user)
        
        await db.commit()
        print("SUCCESS: Credentials set for 'admin' with password 'admin123'.")

if __name__ == "__main__":
    asyncio.run(set_admin_credentials())
