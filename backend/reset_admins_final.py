import asyncio
from database import SessionLocal
from models import User
from auth import get_password_hash
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

async def reset_admins():
    async with SessionLocal() as db:
        print("1. Deleting ALL existing admins...")
        # Delete anyone who is an admin or super admin
        await db.execute(delete(User).where((User.is_admin == True) | (User.is_super_admin == True)))
        
        print("2. Creating Super Admin 'abdelaali'...")
        super_admin = User(
            username="abdelaali",
            hashed_password=get_password_hash("abcd1234!@#$"),
            email="abdelaali.markabi@gmail.com",
            first_name="Abdelaali",
            last_name="Markabi",
            phone_number="0000000000",
            is_admin=True,
            is_super_admin=True,
            is_active=True
        )
        db.add(super_admin)
        
        print("3. Creating Regular Admin 'admin'...")
        regular_admin = User(
            username="admin",
            hashed_password=get_password_hash("admin1234"),
            email="admin.local@example.com", # Must be unique
            first_name="Admin",
            last_name="User",
            phone_number="1111111111",
            is_admin=True,
            is_super_admin=False, # Explicitly False
            is_active=True
        )
        db.add(regular_admin)
        
        await db.commit()
        print("SUCCESS: Admin accounts reset to final specification.")

if __name__ == "__main__":
    asyncio.run(reset_admins())
