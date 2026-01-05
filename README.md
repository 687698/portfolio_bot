# Telegram Community Management Bot

A professional Telegram bot designed for managing large community groups (4000+ members) with features for moderation, user management, and message logging.

## Project Structure

```
pro_telegram_bot/
├── .env                          # Environment variables (create from .env.template)
├── requirements.txt              # Python dependencies
├── README.md                     # This file
└── src/
    ├── bot.py                   # Main bot entry point
    ├── database.py              # Supabase database handling
    └── handlers/                # Command and message handlers
        ├── __init__.py
        ├── commands.py          # Bot commands (/start, /help, etc.)
        ├── message_handler.py   # Message processing and logging
        └── moderation.py        # Moderation functions
```

## Setup Instructions

### 1. Clone/Create the Project
```bash
cd pro_telegram_bot
```

### 2. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
# or
source venv/bin/activate  # On macOS/Linux
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.template` to `.env` and fill in your credentials:
```bash
cp .env .env
```

Then edit `.env` with:
- Your Telegram Bot Token (from BotFather)
- Your Supabase URL
- Your Supabase API Key
- Your Admin Telegram ID

### 5. Setup Supabase Tables

Create the following tables in your Supabase project:

**users table:**
```sql
CREATE TABLE users (
  id BIGSERIAL PRIMARY KEY,
  user_id BIGINT UNIQUE NOT NULL,
  username VARCHAR(255),
  first_name VARCHAR(255),
  last_name VARCHAR(255),
  joined_at TIMESTAMP DEFAULT NOW()
);
```

**warnings table:**
```sql
CREATE TABLE warnings (
  id BIGSERIAL PRIMARY KEY,
  user_id BIGINT REFERENCES users(user_id),
  reason TEXT,
  admin_id BIGINT,
  warned_at TIMESTAMP DEFAULT NOW()
);
```

**message_logs table:**
```sql
CREATE TABLE message_logs (
  id BIGSERIAL PRIMARY KEY,
  user_id BIGINT REFERENCES users(user_id),
  message_id BIGINT,
  text TEXT,
  chat_id BIGINT,
  logged_at TIMESTAMP DEFAULT NOW()
);
```

### 6. Run the Bot
```bash
python src/bot.py
```

## Features

- ✅ User management and tracking
- ✅ Message logging and monitoring
- ✅ Warning system for rule violations
- ✅ New member welcome handling
- ✅ Admin commands
- ✅ Statistics and reporting

## Next Steps

Tell me what specific features you'd like to add to your bot, and I'll implement them!
