# ⚡ QUICK START GUIDE

## 🎯 Get Your Bot Running in 5 Minutes

### **Prerequisites (Before You Start)**
- ✅ Telegram bot token (from BotFather)
- ✅ Supabase URL
- ✅ Supabase API Key
- ✅ Your Telegram user ID
- ✅ Python installed on Windows

---

## 📋 5-Step Installation

### **Step 1: Open PowerShell**
```powershell
cd C:\Users\NIMA99\Desktop\pro_telegram_bot
```

### **Step 2: Create & Activate Virtual Environment**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```
✅ You should see `(venv)` in your prompt

### **Step 3: Install Dependencies**
```powershell
pip install -r requirements.txt
```
⏳ Wait ~2-3 minutes for installation to complete

### **Step 4: Configure .env File**
Open `.env` in any text editor and replace:
```
TELEGRAM_TOKEN=your_token_here
SUPABASE_URL=your_url_here
SUPABASE_KEY=your_key_here
BOT_ADMIN_ID=your_telegram_id_here
LOG_LEVEL=INFO
```

### **Step 5: Run the Bot**
```powershell
python src/bot.py
```

✅ **Done!** Your bot is now running!

---

## 🧪 Quick Test

Open Telegram and go to your group:

1. Type `/start` → Bot welcomes you
2. Type `/stats` → Shows your warnings
3. Post any link → Should be deleted + warning
4. Post any banned word → Should be deleted + warning
5. As admin: Reply to message with `/warn` → Warns user

**All warnings auto-delete after 10 seconds**

---

## 🛑 Stop the Bot

In PowerShell, press: `Ctrl + C`

---

## 🔐 Keep Your Credentials Safe

⚠️ **IMPORTANT:**
- `.env` contains your secrets
- Never share or upload it
- It's in `.gitignore` to prevent accidents
- Never put credentials in code files

---

## 🆘 If Something Goes Wrong

**Error: "ModuleNotFoundError"**
```
→ Check (venv) in prompt
→ Run: pip install -r requirements.txt
```

**Error: "TELEGRAM_TOKEN must be set"**
```
→ Check .env file exists in root folder
→ Check you filled in actual credentials (not placeholders)
```

**Error: "No module named 'src'"**
```
→ Make sure you're in: C:\Users\NIMA99\Desktop\pro_telegram_bot
→ Not in the src folder
```

**Bot not responding in group:**
```
→ Make sure bot is added to the group
→ Make sure bot has admin permissions
→ Check token is correct
```

---

## 📊 What Your Bot Does

✅ **Spam & Profanity Filter**
- Detects URLs (http://, t.me, bit.ly, .com, .ir, etc.)
- Filters 44 banned words (Persian spam & profanity)
- Auto-deletes messages + sends warning
- Warnings auto-delete after 10 seconds

✅ **User Management**
- Tracks users in database
- Counts warnings
- Auto-mutes after 3 warnings
- Ban/unmute commands for admins

✅ **Admin Commands**
- `/warn` - Warn users (3 = mute)
- `/ban` - Ban permanently
- `/unmute` - Remove restrictions
- `/addword word` - Add new banned word

✅ **User Commands**
- `/start` - Welcome message
- `/help` - Show menu
- `/stats` - Your warning count

---

## 🚀 Next: Deploy to Production

For 24/7 hosting (not local testing):
- Railway.app
- Render.com
- Heroku
- AWS Lambda
- Google Cloud Functions

Just deploy this same code to any of these platforms!

---

## 📖 Full Documentation

For detailed information:
- **SETUP_GUIDE.md** - Installation & troubleshooting
- **ANTI_SPAM_GUIDE.md** - How anti-spam works
- **VERIFICATION_REPORT.md** - Code verification
- **CHECKLIST.md** - Pre-launch checklist

---

## 🎉 You're All Set!

Your Persian Telegram bot is ready to manage your 4000-member group!

**Questions?** Check the detailed guides above.

**Happy moderation!** 🛡️
