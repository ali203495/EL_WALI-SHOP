import asyncio
import sys
import os

# Ensure project root is in path
sys.path.append(os.getcwd())

from backend.database import engine
from sqlalchemy import text

async def migrate_wishlist():
    async with engine.begin() as conn:
        print("Checking/Creating wishlists table...")
        
        # Check if column exists (naive check in sqlite, but we are adding a table)
        # For simplicity in this dev environment, just create table if not exists with raw SQL matching the model
        # We rely on sqlalchemy to create it if we use metadata.create_all, but we want to avoid dropping others
        
        await conn.execute(text("""
        CREATE TABLE IF NOT EXISTS wishlists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            product_id INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(product_id) REFERENCES products(id)
        );
        """))
        
        await conn.execute(text("CREATE INDEX IF NOT EXISTS ix_wishlists_id ON wishlists (id);"))
        await conn.execute(text("CREATE INDEX IF NOT EXISTS ix_wishlists_user_id ON wishlists (user_id);"))
        await conn.execute(text("CREATE INDEX IF NOT EXISTS ix_wishlists_product_id ON wishlists (product_id);"))
        
        print("Migration complete.")

if __name__ == "__main__":
    asyncio.run(migrate_wishlist())
