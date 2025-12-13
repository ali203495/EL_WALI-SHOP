import asyncio
import sys
import os

# Ensure project root is in path
sys.path.append(os.getcwd())

from sqlalchemy.future import select
from backend.database import SessionLocal
from backend.models import User
from backend.auth import get_password_hash

async def create_super_admin():
    async with SessionLocal() as session:
        username = "abdelaali"
        password = "acbd1234!@#$"
        
        print(f"Checking for user: {username}")
        result = await session.execute(select(User).where(User.username == username))
        user = result.scalars().first()
        
        hashed_pw = get_password_hash(password)
        
        if user:
            print(f"User {username} exists. Updating credentials...")
            user.hashed_password = hashed_pw
            user.is_admin = True
            user.is_active = True
        else:
            print(f"Creating new super admin: {username}")
            user = User(
                username=username,
                hashed_password=hashed_pw,
                is_admin=True,
                is_active=True
            )
            session.add(user)
            
        await session.commit()
        print("Super admin configured successfully.")

if __name__ == "__main__":
    asyncio.run(create_super_admin())
