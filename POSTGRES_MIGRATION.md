# 🐘 PostgreSQL-Only Configuration

## ✅ What Changed

The Smart Water Saver Agent now **requires PostgreSQL** (no more SQLite option).

### Changes Made:

1. **`database.py`** - Now requires PostgreSQL configuration
2. **`config.py`** - Updated PostgreSQL defaults
3. **New guides created**:
   - `POSTGRES_SETUP.md` - Complete PostgreSQL setup guide
   - `POSTGRES_QUICKSTART.md` - 5-minute quick setup
   - `env.template` - PostgreSQL configuration template

---

## 🚀 Quick Migration Guide

### If You Were Using SQLite Before:

Your old `smart_water_saver.db` file will no longer be used.

### Migration Steps:

#### Step 1: Install PostgreSQL

Follow `POSTGRES_QUICKSTART.md` or `POSTGRES_SETUP.md`

#### Step 2: Create Database

```bash
psql -U postgres
CREATE DATABASE smart_water_saver;
\q
```

#### Step 3: Update .env

Add PostgreSQL configuration:

```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/smart_water_saver
```

#### Step 4: Initialize New Database

```bash
python init_db.py
```

This creates tables in PostgreSQL (optionally with sample data).

#### Step 5: Start Agent

```bash
python main.py
```

---

## 📋 Required .env Configuration

Your `.env` file must now include PostgreSQL configuration:

```env
# REQUIRED: PostgreSQL Configuration
DATABASE_URL=postgresql://postgres:password@localhost:5432/smart_water_saver

# Or use individual settings:
# DB_HOST=localhost
# DB_PORT=5432
# DB_NAME=smart_water_saver
# DB_USER=postgres
# DB_PASSWORD=your_password_here

# Other configurations (Gemini, Weather, etc.)
LLM_PROVIDER=gemini
GOOGLE_API_KEY=your_key_here
WEATHER_PROVIDER=openweather
WEATHER_API_KEY=your_key_here
```

---

## ⚠️ Important Notes

### Database is Required

The agent will **NOT start** without PostgreSQL configuration:

```bash
# This error means PostgreSQL not configured:
ValueError: PostgreSQL database configuration required!
Set DATABASE_URL or individual DB_* variables in .env file.
```

**Solution**: Create `.env` with DATABASE_URL

### No More SQLite

SQLite support has been removed. All data must be in PostgreSQL.

**Why PostgreSQL?**
- ✅ Production-ready
- ✅ Better performance
- ✅ Concurrent access
- ✅ Advanced features
- ✅ Industry standard

---

## 🔧 Troubleshooting

### Error: "PostgreSQL database configuration required!"

**Cause**: No `.env` file or no DATABASE_URL

**Solution**:

```bash
# Copy template
copy env.template .env  # Windows
cp env.template .env    # Linux/Mac

# Edit .env and add:
DATABASE_URL=postgresql://postgres:password@localhost:5432/smart_water_saver
```

### Error: "could not connect to server"

**Cause**: PostgreSQL not installed or not running

**Solution**:

1. Install PostgreSQL (see `POSTGRES_QUICKSTART.md`)
2. Start PostgreSQL service:
   ```bash
   # Windows: Services → PostgreSQL → Start
   # Linux: sudo systemctl start postgresql
   # macOS: brew services start postgresql@16
   ```

### Error: "database 'smart_water_saver' does not exist"

**Solution**:

```bash
psql -U postgres -c "CREATE DATABASE smart_water_saver;"
```

### Error: "password authentication failed"

**Solution**: Use correct password in DATABASE_URL:

```env
DATABASE_URL=postgresql://postgres:CORRECT_PASSWORD@localhost:5432/smart_water_saver
```

---

## 📊 Benefits of PostgreSQL

### Performance

- **Connection pooling**: 10 connections ready to use
- **Concurrent access**: Multiple users simultaneously
- **Optimized queries**: Better than SQLite for analytics

### Scalability

- **Millions of records**: No file size limits
- **Indexes**: Fast queries even with large data
- **Advanced features**: JSON columns, full-text search, etc.

### Production-Ready

- **ACID compliance**: Data integrity guaranteed
- **Backup/Restore**: Enterprise-grade tools
- **Monitoring**: Rich ecosystem of tools
- **Cloud support**: AWS RDS, Google Cloud SQL, etc.

---

## 🎯 Verification Checklist

Before starting the agent:

- [ ] PostgreSQL installed
- [ ] PostgreSQL service running
- [ ] Database `smart_water_saver` created
- [ ] `.env` file with DATABASE_URL
- [ ] `pip install -r requirements.txt` completed
- [ ] Test connection works:
  ```bash
  python -c "from database import db_manager; print('OK')"
  ```

---

## 📚 Documentation

- **Quick Setup**: `POSTGRES_QUICKSTART.md` (5 minutes)
- **Detailed Setup**: `POSTGRES_SETUP.md` (full guide)
- **Dashboard Guide**: `DASHBOARD_GUIDE.md`
- **Environment Template**: `env.template`

---

## 🆘 Need Help?

### Can't Install PostgreSQL?

**Use Cloud PostgreSQL (FREE options)**:
- **Supabase**: https://supabase.com/ (FREE tier)
- **ElephantSQL**: https://www.elephantsql.com/ (FREE tier)
- **Heroku Postgres**: https://www.heroku.com/postgres (FREE tier)

Then use their DATABASE_URL in your `.env`.

### Still Having Issues?

1. Check `POSTGRES_SETUP.md` for detailed troubleshooting
2. Verify PostgreSQL is running: `psql -U postgres -l`
3. Test connection: `python -c "from database import db_manager"`

---

## ✅ Migration Complete!

Once you've:
1. ✅ Installed PostgreSQL
2. ✅ Created database
3. ✅ Configured `.env`
4. ✅ Run `python init_db.py`

You're ready to use the agent with PostgreSQL!

```bash
python main.py
```

Visit: http://localhost:8000/dashboard

**Your agent is now running on production-grade PostgreSQL!** 🐘💧✨

