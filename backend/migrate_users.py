import sqlite3

def migrate():
    print("Migrating users table...")
    conn = sqlite3.connect('/home/xyz/Documents/xxx/pos.db')
    cursor = conn.cursor()
    
    # Check if columns exist
    cursor.execute("PRAGMA table_info(users)")
    columns = [info[1] for info in cursor.fetchall()]
    
    new_columns = {
        'first_name': 'VARCHAR',
        'last_name': 'VARCHAR',
        'email': 'VARCHAR',
        'phone_number': 'VARCHAR',
        'reset_token': 'VARCHAR',
        'reset_token_expiry': 'TIMESTAMP'
    }
    
    for col, dtype in new_columns.items():
        if col not in columns:
            print(f"Adding column {col}...")
            cursor.execute(f"ALTER TABLE users ADD COLUMN {col} {dtype}")
        else:
            print(f"Column {col} already exists.")
            
    conn.commit()
    conn.close()
    print("Migration complete.")

if __name__ == "__main__":
    migrate()
