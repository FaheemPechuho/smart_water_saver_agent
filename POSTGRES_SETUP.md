# 🐘 PostgreSQL Setup Guide

Complete guide to setting up PostgreSQL for the Smart Water Saver Agent.

## 🎯 Why PostgreSQL?

✅ **Production-ready** - Handles concurrent connections  
✅ **Scalable** - Supports millions of records  
✅ **ACID compliant** - Data integrity guaranteed  
✅ **Rich features** - Advanced queries and analytics  
✅ **Industry standard** - Used by major companies  

---

## 🚀 Quick Setup

### Windows

#### Step 1: Download PostgreSQL

1. Go to: https://www.postgresql.org/download/windows/
2. Download the installer (latest version, e.g., PostgreSQL 16)
3. Run the installer

#### Step 2: Installation

1. **Select components**: 
   - ✅ PostgreSQL Server
   - ✅ pgAdmin 4 (GUI tool)
   - ✅ Command Line Tools

2. **Set password**: 
   - Remember this password! (e.g., `postgres123`)

3. **Port**: 
   - Default: `5432` (keep it)

4. **Complete installation**

#### Step 3: Create Database

**Option A: Using pgAdmin (GUI)**

1. Open pgAdmin 4
2. Connect to PostgreSQL server (enter your password)
3. Right-click "Databases" → Create → Database
4. Name: `smart_water_saver`
5. Click "Save"

**Option B: Using Command Line (psql)**

```cmd
# Open Command Prompt as Administrator
cd "C:\Program Files\PostgreSQL\16\bin"

# Connect to PostgreSQL
psql -U postgres

# Enter your password when prompted

# Create database
CREATE DATABASE smart_water_saver;

# Verify
\l

# Exit
\q
```

#### Step 4: Configure .env

Create/update `.env` file in your project:

```env
# ============================================
# PostgreSQL Database Configuration
# ============================================

# Option 1: Full connection string (recommended)
DATABASE_URL=postgresql://postgres:postgres123@localhost:5432/smart_water_saver

# Option 2: Individual settings (alternative)
# DB_HOST=localhost
# DB_PORT=5432
# DB_NAME=smart_water_saver
# DB_USER=postgres
# DB_PASSWORD=postgres123

# Other configurations
LLM_PROVIDER=gemini
GOOGLE_API_KEY=your_gemini_key_here
WEATHER_PROVIDER=openweather
WEATHER_API_KEY=your_weather_key_here
```

**Replace `postgres123` with your actual PostgreSQL password!**

---

### Linux (Ubuntu/Debian)

#### Step 1: Install PostgreSQL

```bash
# Update package list
sudo apt update

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Start PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

#### Step 2: Create Database and User

```bash
# Switch to postgres user
sudo -u postgres psql

# In PostgreSQL prompt:
# Create database
CREATE DATABASE smart_water_saver;

# Create user (optional - or use postgres user)
CREATE USER water_admin WITH PASSWORD 'your_secure_password';

# Grant privileges
GRANT ALL PRIVILEGES ON DATABASE smart_water_saver TO water_admin;

# Exit
\q
```

#### Step 3: Configure .env

```env
# Using custom user
DATABASE_URL=postgresql://water_admin:your_secure_password@localhost:5432/smart_water_saver

# Or using postgres user
# DATABASE_URL=postgresql://postgres:postgres@localhost:5432/smart_water_saver
```

---

### macOS

#### Step 1: Install PostgreSQL

```bash
# Using Homebrew
brew install postgresql@16

# Start PostgreSQL
brew services start postgresql@16
```

#### Step 2: Create Database

```bash
# Create database
createdb smart_water_saver

# Or using psql
psql postgres

# In psql:
CREATE DATABASE smart_water_saver;
\q
```

#### Step 3: Configure .env

```env
DATABASE_URL=postgresql://yourusername@localhost:5432/smart_water_saver
```

(Replace `yourusername` with your Mac username)

---

## 🔧 Verify Installation

### Test PostgreSQL Connection

```bash
# Windows (in PostgreSQL bin directory)
psql -U postgres -d smart_water_saver

# Linux/Mac
psql -U postgres -d smart_water_saver
# or
psql smart_water_saver
```

You should see:
```
smart_water_saver=#
```

Type `\q` to exit.

---

## 🚀 Initialize Agent Database

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

This installs `psycopg2-binary` and `sqlalchemy`.

### Step 2: Initialize Tables

```bash
python init_db.py
```

This will:
- ✅ Connect to PostgreSQL
- ✅ Create all 5 tables
- ✅ Optionally add sample data

### Step 3: Start the Agent

```bash
python main.py
```

You should see:
```
INFO: Database tables initialized
INFO: Starting SmartWaterSaverAgent
```

---

## 📝 .env File Templates

### Template 1: Full Connection String (Recommended)

```env
# ============================================
# Smart Water Saver Agent - PostgreSQL Config
# ============================================

# Database (PostgreSQL - REQUIRED)
DATABASE_URL=postgresql://username:password@host:port/database_name

# Example:
# DATABASE_URL=postgresql://postgres:mypassword@localhost:5432/smart_water_saver

# LLM Configuration
LLM_PROVIDER=gemini
GOOGLE_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash-preview-09-2025

# Weather Configuration
WEATHER_PROVIDER=openweather
WEATHER_API_KEY=your_openweather_api_key_here
```

### Template 2: Individual Settings

```env
# Database Configuration (PostgreSQL)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=smart_water_saver
DB_USER=postgres
DB_PASSWORD=your_postgres_password_here

# LLM and Weather (same as above)
LLM_PROVIDER=gemini
GOOGLE_API_KEY=your_gemini_api_key_here
WEATHER_PROVIDER=openweather
WEATHER_API_KEY=your_openweather_api_key_here
```

---

## 🔍 Troubleshooting

### Error: "PostgreSQL database configuration required!"

**Cause**: No database configuration in `.env`

**Solution**: Create `.env` file with DATABASE_URL:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/smart_water_saver
```

### Error: "could not connect to server"

**Cause**: PostgreSQL service not running

**Solution**:

```bash
# Windows
# Open Services → Find PostgreSQL → Start

# Linux
sudo systemctl start postgresql
sudo systemctl status postgresql

# macOS
brew services start postgresql@16
```

### Error: "password authentication failed"

**Cause**: Wrong password in DATABASE_URL

**Solution**: Use correct password you set during installation:

```env
DATABASE_URL=postgresql://postgres:YOUR_CORRECT_PASSWORD@localhost:5432/smart_water_saver
```

### Error: "database does not exist"

**Cause**: Database not created

**Solution**:

```bash
# Using psql
psql -U postgres
CREATE DATABASE smart_water_saver;
\q

# Or using createdb
createdb -U postgres smart_water_saver
```

### Error: "psycopg2 not installed"

**Cause**: Missing Python PostgreSQL driver

**Solution**:

```bash
pip install psycopg2-binary
# or
pip install -r requirements.txt
```

### Error: "Peer authentication failed" (Linux)

**Cause**: PostgreSQL using peer authentication

**Solution**: Edit `pg_hba.conf`:

```bash
# Find pg_hba.conf location
sudo -u postgres psql -c "SHOW hba_file"

# Edit it
sudo nano /etc/postgresql/16/main/pg_hba.conf

# Change this line:
# local   all             all                                     peer

# To this:
local   all             all                                     md5

# Restart PostgreSQL
sudo systemctl restart postgresql
```

---

## 🗄️ Database Management

### View Tables

```bash
psql -U postgres -d smart_water_saver

# List tables
\dt

# Describe table structure
\d users
\d water_usage

# Exit
\q
```

### Query Data

```sql
-- Connect to database
psql -U postgres -d smart_water_saver

-- See all users
SELECT * FROM users;

-- Count conversations
SELECT COUNT(*) FROM conversation_logs;

-- Total water usage
SELECT user_id, SUM(usage_liters) as total 
FROM water_usage 
GROUP BY user_id;

-- Exit
\q
```

### Backup Database

```bash
# Backup
pg_dump -U postgres smart_water_saver > backup.sql

# Restore
psql -U postgres smart_water_saver < backup.sql
```

### Reset Database

```bash
# Drop and recreate
psql -U postgres

DROP DATABASE smart_water_saver;
CREATE DATABASE smart_water_saver;
\q

# Then reinitialize
python init_db.py
```

---

## 🔐 Security Best Practices

### 1. Strong Password

```env
# Bad
DATABASE_URL=postgresql://postgres:postgres@localhost/smart_water_saver

# Good
DATABASE_URL=postgresql://postgres:Xk9$mP2#vQ7@wZ@localhost/smart_water_saver
```

### 2. Create Dedicated User

Don't use `postgres` superuser for the app:

```sql
CREATE USER water_app WITH PASSWORD 'strong_password_here';
GRANT ALL PRIVILEGES ON DATABASE smart_water_saver TO water_app;
```

Then use:
```env
DATABASE_URL=postgresql://water_app:strong_password_here@localhost/smart_water_saver
```

### 3. Never Commit .env

Ensure `.gitignore` includes:
```
.env
*.env
.env.*
```

### 4. Use Environment Variables

For production, use system environment variables instead of `.env`:

```bash
# Linux/Mac
export DATABASE_URL="postgresql://..."

# Windows PowerShell
$env:DATABASE_URL="postgresql://..."
```

---

## 🌐 Remote PostgreSQL (Optional)

### Using Cloud PostgreSQL

**Popular providers:**
- **AWS RDS** - https://aws.amazon.com/rds/postgresql/
- **Google Cloud SQL** - https://cloud.google.com/sql/postgresql
- **Azure Database** - https://azure.microsoft.com/en-us/products/postgresql
- **DigitalOcean** - https://www.digitalocean.com/products/managed-databases-postgresql
- **Heroku Postgres** - https://www.heroku.com/postgres
- **Supabase** - https://supabase.com/ (FREE tier available!)

### Connection String Format

```env
DATABASE_URL=postgresql://user:password@host.provider.com:5432/dbname?sslmode=require
```

Example (Supabase):
```env
DATABASE_URL=postgresql://postgres:password@db.xxx.supabase.co:5432/postgres
```

### SSL Configuration

For cloud databases, you may need SSL:

```python
# In database.py, add:
from sqlalchemy.engine.url import make_url

url = make_url(db_url)
if url.host != 'localhost':
    connect_args = {"sslmode": "require"}
    self.engine = create_engine(db_url, connect_args=connect_args)
```

---

## 📊 Performance Tuning

### Connection Pooling

Already configured in `database.py`:

```python
self.engine = create_engine(
    db_url,
    pool_size=10,        # Number of connections in pool
    max_overflow=20,     # Maximum additional connections
    pool_pre_ping=True   # Verify connections are alive
)
```

### Indexes (Advanced)

For better performance with large datasets:

```sql
-- Connect to database
psql -U postgres -d smart_water_saver

-- Add indexes
CREATE INDEX idx_water_usage_user_date ON water_usage(user_id, date);
CREATE INDEX idx_conv_logs_user_time ON conversation_logs(user_id, timestamp);
CREATE INDEX idx_weather_loc_date ON weather_history(location, date);

-- View indexes
\di
```

---

## ✅ Verification Checklist

Before starting the agent:

- [ ] PostgreSQL installed and running
- [ ] Database `smart_water_saver` created
- [ ] `.env` file created with DATABASE_URL
- [ ] `pip install -r requirements.txt` completed
- [ ] `python init_db.py` ran successfully
- [ ] Can connect with `psql -U postgres -d smart_water_saver`

Test connection:
```bash
python -c "from database import db_manager; print('✅ Database connection successful!')"
```

---

## 🎉 You're Ready!

### Start the Agent

```bash
python main.py
```

### Access Dashboard

```
http://localhost:8000/dashboard
```

### Check Database

```bash
psql -U postgres -d smart_water_saver
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM conversation_logs;
\q
```

---

## 📚 Additional Resources

- **PostgreSQL Docs**: https://www.postgresql.org/docs/
- **pgAdmin**: https://www.pgadmin.org/
- **SQLAlchemy Docs**: https://docs.sqlalchemy.org/
- **psycopg2 Docs**: https://www.psycopg.org/docs/

---

**Status: ✅ PostgreSQL-Only Configuration Complete!**

Your Smart Water Saver Agent now uses production-ready PostgreSQL! 🐘💧✨

