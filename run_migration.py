import sqlite3
import os

def run_migration():
    # Get the absolute path to the database file
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.db')
    
    # Check if database exists
    if not os.path.exists(db_path):
        print("Database file not found. Please make sure the application has been run at least once.")
        return
    
    # Read the migration SQL
    migration_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'migrate_add_linha.sql')
    
    try:
        with open(migration_script, 'r', encoding='utf-8') as f:
            sql_commands = f.read()
        
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Execute the migration script
        print("Running migration...")
        cursor.executescript(sql_commands)
        
        # Verify the changes
        cursor.execute("PRAGMA table_info(pedidos)")
        columns = cursor.fetchall()
        print("\nTable 'pedidos' now has the following columns:")
        for col in columns:
            print(f"- {col[1]} ({col[2]})")
        
        # Commit changes and close connection
        conn.commit()
        print("\nMigration completed successfully!")
        
    except Exception as e:
        print(f"Error during migration: {e}")
        if 'conn' in locals():
            conn.rollback()
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    print("=== Database Migration Tool ===")
    print("This script will add a 'linha' column to the 'pedidos' table.")
    print("Make sure to back up your database before proceeding!")
    
    confirm = input("\nDo you want to continue? (yes/no): ").strip().lower()
    if confirm == 'yes' or confirm == 'y':
        run_migration()
    else:
        print("Migration cancelled.")
