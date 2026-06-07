"""Startup check script to verify database connection before starting API."""

import os
import sys
from src.config import settings
from src.database import check_database_connection, create_database_tables

def main():
    print("=" * 50)
    print("Project Manager - Startup Check")
    print("=" * 50)
    
    # Check environment
    print("\n📋 Environment Check:")
    print(f"  DATABASE_URL configured: {'Yes' if os.getenv('DATABASE_URL') else 'No (using individual params)'}")
    print(f"  POSTGRES_HOST: {settings.postgres_host}")
    print(f"  POSTGRES_PORT: {settings.postgres_port}")
    print(f"  POSTGRES_DB: {settings.postgres_db}")
    print(f"  POSTGRES_USER: {settings.postgres_user}")
    print(f"  MCP_SERVER_NAME: {settings.mcp_server_name}")
    
    # Check database connection
    print("\n🔌 Database Connection Check:")
    try:
        result = check_database_connection()
        print(f"  ✅ Database connected: {result}")
    except Exception as e:
        print(f"  ❌ Database connection failed: {e}")
        print("\n💡 Troubleshooting:")
        print("  - Check DATABASE_URL environment variable")
        print("  - Verify Supabase project is active")
        print("  - Ensure password is correct (URL-encoded if needed)")
        sys.exit(1)
    
    # Check/create tables
    print("\n🗄️  Database Tables:")
    try:
        create_database_tables()
        print("  ✅ Tables verified/created")
    except Exception as e:
        print(f"  ⚠️  Table check warning: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Startup check complete - starting application")
    print("=" * 50)
    return 0

if __name__ == "__main__":
    sys.exit(main())
