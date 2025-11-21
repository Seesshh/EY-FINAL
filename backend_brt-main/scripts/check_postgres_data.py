#!/usr/bin/env python
"""
Script to check PostgreSQL database tables and their contents.
This will help us understand the state of the PostgreSQL database.
"""

import sys
from pathlib import Path
from sqlalchemy import inspect, text

# Add parent directory to path so we can import app modules
sys.path.append(str(Path(__file__).parent.parent))

# Import app modules
from app.db.postgres import SessionLocal, engine, Base
from app.core.config import settings

def check_postgres_connection():
    """Check if we can connect to PostgreSQL"""
    print("Checking PostgreSQL connection...")
    
    try:
        # Try to connect to PostgreSQL
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1")).fetchone()
            if result and result[0] == 1:
                print("✅ Successfully connected to PostgreSQL")
                return True
            else:
                print("❌ Failed to verify PostgreSQL connection")
                return False
    except Exception as e:
        print(f"❌ Error connecting to PostgreSQL: {str(e)}")
        return False

def list_tables():
    """List all tables in the PostgreSQL database"""
    print("\nListing PostgreSQL tables...")
    
    try:
        # Get inspector
        inspector = inspect(engine)
        
        # Get table names
        tables = inspector.get_table_names()
        
        if not tables:
            print("No tables found in the database.")
            return []
        
        print(f"Found {len(tables)} tables:")
        for table in tables:
            print(f"  - {table}")
        
        return tables
    
    except Exception as e:
        print(f"Error listing tables: {str(e)}")
        return []

def check_table_contents(table_name):
    """Check the contents of a specific table"""
    print(f"\nChecking contents of table '{table_name}'...")
    
    db = SessionLocal()
    try:
        # Count rows
        count_query = text(f"SELECT COUNT(*) FROM {table_name}")
        count = db.execute(count_query).scalar()
        
        print(f"Table '{table_name}' has {count} rows")
        
        if count > 0:
            # Get sample rows
            sample_query = text(f"SELECT * FROM {table_name} LIMIT 5")
            rows = db.execute(sample_query).fetchall()
            
            print(f"\nSample rows from '{table_name}':")
            
            # Get column names
            columns = db.execute(text(f"SELECT * FROM {table_name} LIMIT 0")).keys()
            
            # Print column names
            print("  | " + " | ".join(str(col) for col in columns) + " |")
            print("  | " + " | ".join("-" * len(str(col)) for col in columns) + " |")
            
            # Print rows
            for row in rows:
                print("  | " + " | ".join(str(val)[:30] + ("..." if len(str(val)) > 30 else "") for val in row) + " |")
            
            if count > 5:
                print(f"  ... and {count - 5} more rows")
        
        return count
    
    except Exception as e:
        print(f"Error checking table contents: {str(e)}")
        return 0
    finally:
        db.close()

def create_tables():
    """Create tables if they don't exist"""
    print("\nCreating tables if they don't exist...")
    
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully")
        return True
    
    except Exception as e:
        print(f"Error creating tables: {str(e)}")
        return False

def main():
    """Main function"""
    print("PostgreSQL Database Check")
    print("========================\n")
    
    # Step 1: Check PostgreSQL connection
    connection_ok = check_postgres_connection()
    if not connection_ok:
        print("Cannot proceed without PostgreSQL connection. Exiting.")
        return
    
    # Step 2: List tables
    tables = list_tables()
    
    # Step 3: Create tables if they don't exist
    if not tables:
        print("\nNo tables found. Creating tables...")
        create_tables()
        tables = list_tables()
    
    # Step 4: Check table contents
    if tables:
        for table in tables:
            check_table_contents(table)
    
    print("\nPostgreSQL Database Check Completed")
    print("================================")

if __name__ == "__main__":
    main()
