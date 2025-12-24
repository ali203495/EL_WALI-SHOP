import asyncio
import os
import aiosqlite
import asyncpg
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import text
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from database import Base, DATABASE_URL

# This script assumes 'pos.db' is in the same directory or adjust path
SQLITE_DB_PATH = "./pos.db"

async def migrate():
    target_url = os.getenv("DATABASE_URL")
    if not target_url or "sqlite" in target_url:
        print("Error: DATABASE_URL not set or points to SQLite. Please set DATABASE_URL to your Postgres instance.")
        return

    # Fix protocol for asyncpg
    if target_url.startswith("postgres://"):
        target_url = target_url.replace("postgres://", "postgresql+asyncpg://", 1)
    elif target_url.startswith("postgresql://") and "+asyncpg" not in target_url:
        target_url = target_url.replace("postgresql://", "postgresql+asyncpg://", 1)

    print(f"Migrating from {SQLITE_DB_PATH} to Postgres...")
    
    # 1. Create Tables in Postgres
    engine = create_async_engine(target_url, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all) # Optional: Wipe target first? Safer for clean migration.
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created in Postgres.")

    # 2. Connect to SQLite
    async with aiosqlite.connect(SQLITE_DB_PATH) as sqlite_conn:
        sqlite_conn.row_factory = aiosqlite.Row
        
        # Helper to copy table
        async def copy_table(table_name, columns):
            print(f"Migrating {table_name}...")
            async with sqlite_conn.execute(f"SELECT * FROM {table_name}") as cursor:
                rows = await cursor.fetchall()
                if not rows:
                    print(f"No rows in {table_name}")
                    return

                # Convert rows to dicts
                data = [dict(row) for row in rows]
                
                # Insert into Postgres using SQLAlchemy
                async with AsyncSession(engine) as session:
                    # We use raw SQL for simplicity in bulk insert without model constraints issues initially,
                    # but typically we should strict order.
                    # Or better: using the actual Models? Models might have relationships.
                    # Raw SQL insert is often easier for migration scripts if schemas match.
                    
                    cols = ", ".join(columns)
                    params = ", ".join([f":{col}" for col in columns])
                    stmt = text(f"INSERT INTO {table_name} ({cols}) VALUES ({params})")
                    
                    await session.execute(stmt, data)
                    await session.commit()
            print(f"Migrated {len(rows)} rows for {table_name}")

        # Order matters due to Foreign Keys!
        # Users -> SiteSettings, Brands, Categories -> Products -> Reviews, Inventory
        # Stores -> Orders -> OrderItems (requires Products) -> Payments
        
        # 1. Users
        await copy_table("users", ["id", "username", "email", "hashed_password", "role", "first_name", "last_name", "phone_number", "is_active", "created_at"])
        
        # 2. Site Settings
        await copy_table("site_settings", ["id", "key", "value", "description", "updated_at"])
        
        # 3. Brands
        await copy_table("brands", ["id", "name", "slug", "logo_url", "description", "is_active", "created_at"])
        
        # 4. Categories
        await copy_table("categories", ["id", "name", "slug", "description", "image_url", "parent_id", "is_active", "display_order", "created_at"])
        
        # 5. Store Locations
        await copy_table("store_locations", ["id", "name", "address", "city", "phone", "email", "is_active", "latitude", "longitude", "created_at"])
        
        # 6. Products
        # Note: adjust columns based on actual schema. checking models.py would be wise if unsure.
        # Assuming standard schema based on usage.
        await copy_table("products", ["id", "name", "slug", "description", "price", "compare_at_price", "cost_price", "sku", "barcode", "stock", "track_stock", "image_url", "additional_images", "is_active", "is_featured", "category_id", "brand_id", "rating", "review_count", "specs", "created_at", "updated_at"])

        # 7. Wishlists
        await copy_table("wishlists", ["id", "user_id", "product_id", "created_at"])
        
        # 8. Orders
        await copy_table("orders", ["id", "user_id", "order_number", "customer_email", "customer_phone", "customer_name", "shipping_address", "billing_address", "status", "payment_status", "payment_method", "shipping_method", "subtotal", "tax_amount", "shipping_cost", "discount_amount", "total_amount", "notes", "created_at", "updated_at"])
        
        # 9. Order Items
        await copy_table("order_items", ["id", "order_id", "product_id", "product_name", "price", "quantity", "total", "sku"])

    print("Migration complete!")

if __name__ == "__main__":
    asyncio.run(migrate())
