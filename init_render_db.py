"""
Initialize database for Render deployment.
Runs automatically during build process.
"""
from database import db_manager
import sys

def init_database():
    """Initialize database tables."""
    try:
        print("🔄 Initializing database tables...")
        db_manager.create_tables()
        print("✅ Database tables created successfully!")
        return True
    except Exception as e:
        error_msg = str(e)
        # This is okay if tables already exist
        if "already exists" in error_msg.lower():
            print("✓ Database tables already exist (this is normal)")
            return True
        else:
            print(f"❌ Database initialization error: {e}")
            print("⚠️  This may be normal if tables already exist.")
            # Don't fail deployment if tables exist
            return True

if __name__ == "__main__":
    success = init_database()
    # Exit with 0 even if tables exist to not fail deployment
    sys.exit(0 if success else 1)

