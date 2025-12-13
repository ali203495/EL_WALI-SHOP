import asyncio
from database import SessionLocal
from models import Category
from sqlalchemy import select, func

async def check():
    async with SessionLocal() as db:
        result = await db.execute(select(func.count(Category.id)))
        count = result.scalar()
        print(f"Categories count: {count}")
        
        result = await db.execute(select(Category.name))
        names = result.scalars().all()
        print(f"Categories: {names}")

if __name__ == "__main__":
    asyncio.run(check())
