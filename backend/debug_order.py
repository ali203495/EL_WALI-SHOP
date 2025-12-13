import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import SessionLocal
from backend.models import Order, OrderItem, Product
from sqlalchemy import select
from sqlalchemy.orm import selectinload

async def test_order_creation():
    print("🔄 Connecting to database...")
    async with SessionLocal() as db:
        try:
            # 1. Fetch a product
            print("Fetching product...")
            result = await db.execute(select(Product).limit(1))
            product = result.scalars().first()
            
            if not product:
                print("❌ No products found!")
                return

            print(f"✅ Found product: {product.name} (ID: {product.id}, Price: {product.price}, Stock: {product.stock})")

            # 2. Simulate Order Creation
            print("🛒 simulating create_order...")
            
            # Start transaction
            db_order = Order(status="completed")
            db.add(db_order)
            await db.flush()
            print(f"Created Order ID: {db_order.id}")

            # Add Item
            qty = 1
            if product.stock < qty:
                 print("Not enough stock")
                 return
            
            product.stock -= qty
            
            db_item = OrderItem(
                order_id=db_order.id,
                product_id=product.id,
                quantity=qty,
                price_at_time=product.price
            )
            db.add(db_item)
            
            db_order.total_amount = product.price * qty
            
            # Cache ID before commit (which expires the object)
            order_id = db_order.id
            
            print("Committing...")
            await db.commit()
            print("✅ Commit success!")
            
            # 3. Simulate Re-fetch (API Logic)
            print("🔄 Re-fetching with selectinload...")
            result = await db.execute(
                select(Order)
                .options(selectinload(Order.items))
                .where(Order.id == order_id)
            )
            order = result.scalars().first()
            print(f"✅ Retrieved Order: {order.id}, Items: {len(order.items)}")
            
            # 4. Dump Pydantic Schema (Simulate Response validation)
            # We don't have the full app context here but we can try basic attribute access
            for item in order.items:
                print(f"   - Item: Product {item.product_id}, Qty {item.quantity}, Price {item.price_at_time}")
                
        except Exception as e:
            print(f"❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
            await db.rollback()

if __name__ == "__main__":
    asyncio.run(test_order_creation())
