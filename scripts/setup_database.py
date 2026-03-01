"""
Database Setup Script

This script creates the Snowflake database with all required tables and views,
loads the resolved tickets CSV data, and creates Cortex Search Services.
Run this script to initialize your complete database setup.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

from backend.db.snowflake_utils import get_session
from backend.db.sql_utils import execute_sql_file


def load_resolved_tickets_data(session):
    """Load CSV data into RESOLVED_TICKETS table"""
    
    # Get CSV file path
    csv_path = Path(__file__).parent.parent / "backend" / "db" / "csv" / "aa_dataset-tickets-multi-lang-5-2-50-version.csv"
    
    if not csv_path.exists():
        print(f"     ⚠️  Warning: CSV file not found at {csv_path}")
        print(f"     ⏭️  Skipping data loading")
        return
    
    try:
        # Create file format
        print(f"     📋 Creating CSV file format...")
        session.sql("""
            CREATE OR REPLACE FILE FORMAT csv_format
            TYPE = 'CSV'
            FIELD_DELIMITER = ','
            SKIP_HEADER = 1
            FIELD_OPTIONALLY_ENCLOSED_BY = '"'
            ESCAPE_UNENCLOSED_FIELD = NONE
            ENCODING = 'UTF8'
            NULL_IF = ('', 'NULL')
        """).collect()
        
        # Upload file to user stage
        print(f"     ⬆️  Uploading CSV file to Snowflake stage...")
        session.file.put(
            str(csv_path),
            "@~",
            auto_compress=False,
            overwrite=True
        )
        
        # Truncate existing data
        print(f"     🗑️  Clearing existing data...")
        session.sql("TRUNCATE TABLE IF EXISTS RESOLVED_TICKETS").collect()
        
        # Load data from stage
        print(f"     📊 Loading data into table...")
        copy_result = session.sql(f"""
            COPY INTO RESOLVED_TICKETS
            FROM @~/{csv_path.name}
            FILE_FORMAT = csv_format
            ON_ERROR = 'CONTINUE'
        """).collect()
        
        # Display results
        for row in copy_result:
            print(f"     ✅ Loaded {row['rows_loaded']} rows")
            if row['errors_seen'] > 0:
                print(f"     ⚠️  Errors: {row['errors_seen']}")
        
    except Exception as e:
        print(f"     ❌ Error loading CSV data: {e}")
        raise


def get_sql_files():
    """Get SQL files organized by directory structure"""
    db_dir = Path(__file__).parent.parent / "backend" / "db"
    
    table_files = sorted((db_dir / "tables").glob("*.sql"))
    view_files = sorted((db_dir / "views").glob("*.sql"))
    cortex_files = sorted((db_dir / "cortex_search_services").glob("*.sql"))
    
    return table_files, view_files, cortex_files


def setup_database_and_schema(session):
    """Create database and schema if they don't exist"""
    database = os.getenv("SNOWFLAKE_DATABASE", "PROJECT_DB")
    schema = os.getenv("SNOWFLAKE_SCHEMA", "PUBLIC")
    
    print(f"📦 Creating database {database}...")
    session.sql(f"CREATE DATABASE IF NOT EXISTS {database}").collect()
    session.sql(f"USE DATABASE {database}").collect()
    
    print(f"📁 Creating schema {schema}...")
    session.sql(f"CREATE SCHEMA IF NOT EXISTS {schema}").collect()
    session.sql(f"USE SCHEMA {schema}").collect()


def create_tables(session):
    """Create all tables"""
    table_files, _, _ = get_sql_files()
    print(f"\n📋 Creating {len(table_files)} table(s)...\n")
    
    for sql_file in table_files:
        print(f"  📄 Creating table from {sql_file.name}...")
        execute_sql_file(session, sql_file)
        print(f"     ✅ {sql_file.name} executed successfully")
    
    return len(table_files)


def create_views(session):
    """Create all views"""
    _, view_files, _ = get_sql_files()
    print(f"\n📋 Creating {len(view_files)} view(s)...\n")
    
    for sql_file in view_files:
        print(f"  📄 Creating view from {sql_file.name}...")
        execute_sql_file(session, sql_file)
        print(f"     ✅ {sql_file.name} executed successfully")
    
    return len(view_files)


def create_cortex_search_services(session):
    """Create all Cortex Search Services"""
    _, _, cortex_files = get_sql_files()
    print(f"\n📋 Creating {len(cortex_files)} cortex search service(s)...\n")
    
    for sql_file in cortex_files:
        print(f"  🔍 Creating cortex search service from {sql_file.name}...")
        execute_sql_file(session, sql_file)
        print(f"     ✅ {sql_file.name} executed successfully")
    
    return len(cortex_files)


def show_menu():
    """Display setup menu and get user choice"""
    print("\n" + "="*60)
    print("🛠️  Snowflake Database Setup")
    print("="*60)
    print("\nChoose a setup option:")
    print("  1. Full setup (all steps)")
    print("  2. Create tables only")
    print("  3. Load CSV data into RESOLVED_TICKETS")
    print("  4. Create views only")
    print("  5. Create Cortex Search Services only")
    print("  6. Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-6): ").strip()
            if choice in ['1', '2', '3', '4', '5', '6']:
                return choice
            print("❌ Invalid choice. Please enter a number between 1 and 6.")
        except KeyboardInterrupt:
            print("\n\n👋 Cancelled by user")
            sys.exit(0)


def run_setup(choice=None):
    """Run database setup based on user choice"""
    
    if choice is None:
        choice = show_menu()
    
    if choice == '6':
        print("\n👋 Exiting...")
        return
    
    print("\n🔌 Connecting to Snowflake...")
    session = get_session()
    
    database = os.getenv("SNOWFLAKE_DATABASE", "PROJECT_DB")
    schema = os.getenv("SNOWFLAKE_SCHEMA", "PUBLIC")
    
    try:
        setup_database_and_schema(session)
        
        table_count = 0
        view_count = 0
        cortex_count = 0
        data_loaded = False
        
        if choice == '1':  # Full setup
            table_count = create_tables(session)
            print(f"\n📥 Loading CSV data into RESOLVED_TICKETS...")
            load_resolved_tickets_data(session)
            data_loaded = True
            view_count = create_views(session)
            cortex_count = create_cortex_search_services(session)
            
        elif choice == '2':  # Tables only
            table_count = create_tables(session)
            
        elif choice == '3':  # Load CSV data
            print(f"\n📥 Loading CSV data into RESOLVED_TICKETS...")
            load_resolved_tickets_data(session)
            data_loaded = True
            
        elif choice == '4':  # Views only
            view_count = create_views(session)
            
        elif choice == '5':  # Cortex Search Services only
            cortex_count = create_cortex_search_services(session)
        
        # Summary
        print("\n" + "="*60)
        print("✨ Setup completed successfully!")
        print("="*60)
        print(f"\n📊 Database: {database}")
        print(f"📂 Schema: {schema}")
        
        if table_count > 0:
            print(f"📋 Tables created: {table_count}")
        if view_count > 0:
            print(f"👁️  Views created: {view_count}")
        if cortex_count > 0:
            print(f"🔍 Cortex Search Services created: {cortex_count}")
        
        # Show data count for RESOLVED_TICKETS
        if data_loaded or choice == '1':
            try:
                count_result = session.sql("SELECT COUNT(*) as count FROM RESOLVED_TICKETS").collect()
                total_records = count_result[0]['COUNT']
                print(f"📥 RESOLVED_TICKETS records loaded: {total_records}")
            except:
                pass
        
    except Exception as e:
        print(f"\n❌ Error during setup: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    # Check if argument provided (for non-interactive use)
    if len(sys.argv) > 1:
        choice = sys.argv[1]
        if choice in ['1', '2', '3', '4', '5', '6']:
            run_setup(choice)
        else:
            print(f"❌ Invalid argument. Use 1-6.")
            sys.exit(1)
    else:
        run_setup()
