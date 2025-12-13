import sqlite3

def migrate():
    print("🔄 Migrating database...")
    try:
        conn = sqlite3.connect("pos.db") 
        cursor = conn.cursor()
        
        # Check if column exists
        cursor.execute("PRAGMA table_info(orders)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if "user_id" not in columns:
            print("➕ Adding user_id column to orders table...")
            cursor.execute("ALTER TABLE orders ADD COLUMN user_id INTEGER REFERENCES users(id)")
            conn.commit()
            print("✅ Migration successful")
        else:
            print("✅ Column user_id already exists")
            
        conn.close()
    except Exception as e:
        print(f"❌ Migration failed: {e}")

if __name__ == "__main__":
    migrate()
