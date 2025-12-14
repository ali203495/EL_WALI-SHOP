import sqlite3

DB_PATH = "backend/pos.db"

def migrate_db():
    print(f"Connecting to {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Check if column exists
        cursor.execute("PRAGMA table_info(users)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if "is_super_admin" not in columns:
            print("Adding 'is_super_admin' column to users table...")
            cursor.execute("ALTER TABLE users ADD COLUMN is_super_admin BOOLEAN DEFAULT 0")
            
            # Set 'admin' and 'Abdelaali' as super admins
            print("Promoting 'admin' and 'Abdelaali' to Super Admin...")
            cursor.execute("UPDATE users SET is_super_admin = 1 WHERE username IN ('admin', 'Abdelaali')")
            
            conn.commit()
            print("Migration successful.")
        else:
            print("'is_super_admin' column already exists.")
            
    except Exception as e:
        print(f"Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_db()
