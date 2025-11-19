"""
Update existing users' locations from London to Islamabad.
Run this once to migrate existing data.
"""
from database import db_manager, User
from sqlalchemy import update

def update_user_locations():
    """Update all users with London location to Islamabad."""
    db = db_manager.get_session()
    
    try:
        # Update all users with London to Islamabad
        result = db.execute(
            update(User)
            .where(User.location == "London")
            .values(location="Islamabad")
        )
        db.commit()
        
        updated_count = result.rowcount
        print(f"✅ Updated {updated_count} user(s) from London to Islamabad")
        
        # Show all users
        users = db.query(User).all()
        print(f"\n📋 Current users:")
        for user in users:
            print(f"  - {user.user_id}: {user.name} ({user.location})")
        
        return True
        
    except Exception as e:
        print(f"❌ Error updating locations: {e}")
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    print("🔄 Updating user locations...")
    success = update_user_locations()
    
    if success:
        print("\n✅ Location update completed!")
    else:
        print("\n❌ Location update failed!")

