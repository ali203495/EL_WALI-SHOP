import sqlite3

def migrate():
    print("🔄 Migrating database (Orders V2)...")
    try:
        conn = sqlite3.connect("pos.db") 
        cursor = conn.cursor()
        
        # Check if column exists
        cursor.execute("PRAGMA table_info(orders)")
        columns = [info[1] for info in cursor.fetchall()]
        
        new_columns = {
            "payment_method": "TEXT DEFAULT 'cod'",
            "customer_email": "TEXT",
            "customer_first_name": "TEXT",
            "customer_last_name": "TEXT",
            "customer_address": "TEXT",
            "customer_city": "TEXT",
            "customer_country": "TEXT",
            "customer_zip": "TEXT"
        }

        for col, dtype in new_columns.items():
            if col not in columns:
                print(f"➕ Adding {col} column to orders table...")
                cursor.execute(f"ALTER TABLE orders ADD COLUMN {col} {dtype}")
                conn.commit()
            else:
                print(f"✅ Column {col} already exists")
            
        conn.close()
        print("✅ Migration V2 successful")
    except Exception as e:
        print(f"❌ Migration failed: {e}")

if __name__ == "__main__":
    migrate()
