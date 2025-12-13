import asyncio
from database import engine, Base
from models import User, Category, Product, Order, OrderItem

async def init_db():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all) # Uncomment to reset
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created.")

if __name__ == "__main__":
    asyncio.run(init_db())
