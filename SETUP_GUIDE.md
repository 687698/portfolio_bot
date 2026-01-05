# 🚀 Complete Setup & Installation Guide

## ✅ Import & Code Verification

All imports in the project are correctly structured:

### **src/bot.py** ✅
- ✅ Imports `load_dotenv` from `python-dotenv`
- ✅ Imports Telegram classes from `python-telegram-bot`
- ✅ Correctly imports handlers from `src.handlers`
- ✅ Initializes DatabaseManager (from src.database)

### **src/database.py** ✅
- ✅ Imports Supabase client
- ✅ Imports `python-dotenv` for environment variables
- ✅ All database methods properly defined

### **src/handlers/** ✅
- ✅ `commands.py` - Imports database and Telegram modules
- ✅ `moderation.py` - All admin functions properly imported
- ✅ `message_handler.py` - Anti-spam filter with regex imports

### **requirements.txt** ✅
```
python-telegram-bot==20.7
python-dotenv==1.0.0
supabase==2.0.3
postgrest-py==0.11.3
```

---

## 🛠️ Step-by-Step Installation & Setup

### **Step 1: Navigate to Project Directory**

Open PowerShell and navigate to your bot folder:

```powershell
cd C:\Users\NIMA99\Desktop\pro_telegram_bot
```

### **Step 2: Create Virtual Environment**

Create an isolated Python environment for the project:

```powershell
python -m venv venv
```

This creates a `venv` folder. You should see:
```
venv/
  ├── Scripts/
  ├── Lib/
  └── pyvenv.cfg
```

### **Step 3: Activate Virtual Environment**

**On Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```

You should see `(venv)` at the start of your terminal prompt:
```
(venv) PS C:\Users\NIMA99\Desktop\pro_telegram_bot>
```

**If activation fails** (ExecutionPolicy error), run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Then try activation again.

### **Step 4: Install Dependencies**

With the virtual environment activated, install all required packages:

```powershell
pip install -r requirements.txt
```

This will install:
- `python-telegram-bot` - Telegram bot library
- `python-dotenv` - Environment variable management
- `supabase` - Supabase Python client
- `postgrest-py` - PostgreSQL REST API client

**Wait for completion** - You'll see:
```
Successfully installed python-telegram-bot-20.7 python-dotenv-1.0.0 supabase-2.0.3 ...
```

### **Step 5: Verify Installation**

Check that all packages installed correctly:

```powershell
pip list
```

You should see all packages listed with correct versions.

---

## 🔐 Environment Variables & .env File

### **Why .env is Important**

Your `.env` file contains sensitive information:
- 🤖 **TELEGRAM_TOKEN** - Your bot's API token
- 🔑 **SUPABASE_KEY** - Database access key
- 📍 **SUPABASE_URL** - Database endpoint

**Never commit this to GitHub or share publicly!**

### **Secure .env Setup**

#### **1. Update .env with Your Credentials**

Edit the `.env` file at the root of your project:

```
# Telegram Bot Configuration
TELEGRAM_TOKEN=your_actual_token_here

# Supabase Configuration
SUPABASE_URL=your_actual_url_here
SUPABASE_KEY=your_actual_key_here

# Bot Settings
BOT_ADMIN_ID=your_telegram_user_id_here
LOG_LEVEL=INFO
```

Replace:
- `your_actual_token_here` → Your Telegram bot token from BotFather
- `your_actual_url_here` → Your Supabase project URL
- `your_actual_key_here` → Your Supabase API key
- `your_telegram_user_id_here` → Your personal Telegram user ID

#### **2. Protect .env File**

Make sure `.env` is in `.gitignore`:

Check if `.gitignore` exists in your project root. If not, create one:

```
# .gitignore
.env
venv/
__pycache__/
*.pyc
.DS_Store
```

**This prevents accidentally uploading your secrets to GitHub.**

#### **3. File Permissions (Windows)**

The `.env` file is automatically private on Windows. Make sure:
- Only your user account can read/write
- It's located in the project root: `C:\Users\NIMA99\Desktop\pro_telegram_bot\.env`

### **How python-dotenv Works**

When the bot starts, this line loads your `.env` file:

```python
load_dotenv()  # In src/bot.py and src/database.py
```

Then your code accesses variables:
```python
token = os.getenv("TELEGRAM_TOKEN")  # Gets value from .env
```

---

## ▶️ Running the Bot Locally

### **Step 1: Ensure Virtual Environment is Active**

Check for `(venv)` in your terminal prompt:
```
(venv) PS C:\Users\NIMA99\Desktop\pro_telegram_bot>
```

If not active, run:
```powershell
venv\Scripts\Activate.ps1
```

### **Step 2: Verify .env File is Configured**

Make sure you've filled in all values in `.env`:
```powershell
cat .env
```

You should see your actual credentials, not the placeholder text.

### **Step 3: Run the Bot**

Start the bot with:

```powershell
python src/bot.py
```

You should see output like:
```
2025-12-29 14:32:15,123 - src.bot - INFO - 🤖 بات شروع شد...
2025-12-29 14:32:16,456 - src.bot - INFO - Bot initialized successfully
2025-12-29 14:32:17,789 - root - INFO - Bot started polling.
```

The bot is now **running and listening** for messages in your Telegram group!

### **Step 4: Test the Bot**

Open Telegram and:

1. **Go to your group**
2. **Type `/start`** → Bot should welcome you
3. **Type `/stats`** → Bot should show your warning count
4. **Post a link** → Bot should delete it + warn
5. **Post a banned word** → Bot should delete it + warn
6. **Reply to a message with `/warn`** (as admin) → Bot should warn user

### **Step 5: Stop the Bot**

Press `Ctrl+C` in the terminal to stop the bot:

```
^C
2025-12-29 14:35:22,890 - telegram.ext._application - INFO - Application stopped.
```

---

## 🔍 Troubleshooting

### **Issue: "ModuleNotFoundError: No module named 'telegram'"**

**Solution:**
1. Check virtual environment is activated (should see `(venv)` in prompt)
2. Reinstall packages:
   ```powershell
   pip install --upgrade -r requirements.txt
   ```

### **Issue: "TELEGRAM_TOKEN must be set in .env file"**

**Solution:**
1. Check `.env` file exists in project root
2. Verify you filled in actual credentials (not placeholders)
3. Make sure `.env` is saved

### **Issue: "SUPABASE_URL and SUPABASE_KEY must be set"**

**Solution:**
1. Get your Supabase credentials from dashboard
2. Add them to `.env`:
   ```
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your-actual-key
   ```
3. Save and restart bot

### **Issue: "No module named 'src'"**

**Solution:**
Make sure you run the bot from the project root:
```powershell
cd C:\Users\NIMA99\Desktop\pro_telegram_bot
python src/bot.py
```

NOT from the `src` folder.

### **Issue: Bot crashes or unresponsive**

**Check the logs:**
- Look for error messages in terminal output
- Check that Telegram token is correct
- Verify Supabase connection by checking `.env` values
- Make sure bot has admin permissions in the group

---

## 📋 Quick Reference Commands

```powershell
# Activate environment
venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run bot
python src/bot.py

# View .env file
cat .env

# List installed packages
pip list

# Deactivate environment
deactivate
```

---

## 🔐 Security Checklist

- ✅ `.env` file created with actual credentials
- ✅ `.env` added to `.gitignore`
- ✅ Virtual environment used (isolated dependencies)
- ✅ No credentials in code files
- ✅ Bot token never shared publicly
- ✅ Supabase key kept private

---

## 🎯 Next Steps

1. ✅ Install dependencies (`pip install -r requirements.txt`)
2. ✅ Configure `.env` with your credentials
3. ✅ Run bot locally (`python src/bot.py`)
4. ✅ Test in your Telegram group
5. ✅ Monitor logs for issues

---

## 📞 Common Issues During Testing

| Issue | Solution |
|-------|----------|
| Bot doesn't respond to commands | Check it's in the group and has admin permissions |
| Warnings not deleting | Check JobQueue is running (should be automatic) |
| Links not detected | Make sure message handler is registered in bot.py |
| Banned words not filtering | Verify words are in Supabase banned_words table |
| Can't run bot | Make sure venv is activated and dependencies installed |

---

## 🚀 Ready to Launch!

Once you see:
```
Bot started polling.
```

Your bot is **live and ready** to manage your group! 🎉

For deployment and production setup, refer to the Telegram Bot documentation or hosting providers like Heroku, Railway, or AWS.
