"""
Database initialization script for Smart Water Saver Agent.
Run this to create all necessary database tables.
"""
from database import db_manager, create_or_update_user, log_water_usage, log_weather
from datetime import datetime, timedelta
import random

def init_database():
    """Initialize the database with tables."""
    print("🔧 Initializing database...")
    db_manager.create_tables()
    print("✅ Database initialized successfully!")
    print(f"📊 Database location: smart_water_saver.db (SQLite)")


def seed_sample_data():
    """Add sample data for testing the dashboard."""
    print("\n🌱 Seeding sample data...")
    
    db = db_manager.get_session()
    
    try:
        # Create sample users
        users = ["user_123", "user_456", "user_789"]
        
        for user_id in users:
            create_or_update_user(
                db,
                user_id=user_id,
                name=f"Test User {user_id.split('_')[1]}",
                email=f"{user_id}@example.com",
                location="London"
            )
            print(f"  ✓ Created user: {user_id}")
        
        # Add sample water usage data (last 30 days)
        print("\n💧 Adding water usage data...")
        for user_id in users:
            for i in range(30):
                date = datetime.utcnow() - timedelta(days=i)
                usage = random.randint(100, 300)  # 100-300 liters per day
                
                log_water_usage(
                    db,
                    user_id=user_id,
                    usage_liters=usage,
                    location="Garden",
                    device="Smart Sprinkler",
                    notes=f"Automated watering day {30-i}"
                )
            
            print(f"  ✓ Added 30 days of usage for {user_id}")
        
        # Add sample weather data
        print("\n🌤️  Adding weather data...")
        locations = ["London", "New York", "Tokyo"]
        for i in range(30):
            date = datetime.utcnow() - timedelta(days=i)
            for location in locations:
                temp = random.uniform(15, 30)
                humidity = random.uniform(40, 80)
                precip = random.uniform(0, 10)
                conditions = ["Clear", "Cloudy", "Rainy", "Partly Cloudy"]
                
                log_weather(
                    db,
                    location=location,
                    temperature=temp,
                    humidity=humidity,
                    precipitation=precip,
                    condition=random.choice(conditions),
                    forecast_data={"source": "sample_data"}
                )
        
        print(f"  ✓ Added 30 days of weather for {len(locations)} locations")
        
        db.commit()
        print("\n✅ Sample data seeded successfully!")
        
    except Exception as e:
        print(f"❌ Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 60)
    print("Smart Water Saver Agent - Database Initialization")
    print("=" * 60)
    
    init_database()
    
    # Ask if user wants sample data
    response = input("\n💡 Would you like to add sample data for testing? (y/n): ")
    if response.lower() in ['y', 'yes']:
        seed_sample_data()
    
    print("\n" + "=" * 60)
    print("🎉 Database setup complete!")
    print("=" * 60)
    print("\n📝 Next steps:")
    print("  1. Run the agent: python main.py")
    print("  2. Visit the dashboard: http://localhost:8000/dashboard")
    print("  3. Use the API: http://localhost:8000/docs")
    print()

