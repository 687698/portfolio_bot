# ✅ Pre-Launch Checklist

## 📋 Code Verification

- ✅ All imports are correct
- ✅ `src/bot.py` imports all handlers properly
- ✅ Database manager imports `python-dotenv` and `supabase`
- ✅ Handler files import `telegram` libraries
- ✅ Anti-spam filter includes URL detection and banned words
- ✅ 44 banned words configured (9 spam + 35 profanity)
- ✅ All Persian messages with RTL formatting
- ✅ Admin-only command visibility configured
- ✅ Auto-delete messages after 5-10 seconds
- ✅ JobQueue for scheduled message deletion

---

## 🛠️ Installation Steps (In Order)

1. **Open PowerShell**
   ```powershell
   cd C:\Users\NIMA99\Desktop\pro_telegram_bot
   ```

2. **Create Virtual Environment**
   ```powershell
   python -m venv venv
   ```

3. **Activate Virtual Environment**
   ```powershell
   venv\Scripts\Activate.ps1
   ```
   (You should see `(venv)` in your prompt)

4. **Install Dependencies**
   ```powershell
   pip install -r requirements.txt
   ```
   Wait for all packages to install successfully.

5. **Configure .env File**
   - Open `.env` in your text editor
   - Replace placeholders with your actual credentials:
     - `TELEGRAM_TOKEN` = Your bot token from BotFather
     - `SUPABASE_URL` = Your Supabase project URL
     - `SUPABASE_KEY` = Your Supabase API key
     - `BOT_ADMIN_ID` = Your Telegram user ID
   - Save the file

6. **Run the Bot**
   ```powershell
   python src/bot.py
   ```
   You should see logs appearing.

---

## 🔐 Security Reminders

⚠️ **IMPORTANT:**
- Never share your `.env` file
- Never commit `.env` to GitHub
- Keep `TELEGRAM_TOKEN` and `SUPABASE_KEY` private
- Only you should have access to `.env`

---

## 🧪 Testing After Launch

Once bot is running:

1. Go to your Telegram group
2. Try `/start` command
3. Try `/help` command
4. Try `/stats` command
5. Post a test link → Should be deleted with warning
6. Post a banned word → Should be deleted with warning
7. As admin, try `/warn` (reply to a message)
8. Check warnings auto-delete after 5-10 seconds

---

## 🆘 If Something Goes Wrong

1. **Check .env file is filled correctly**
   ```powershell
   cat .env
   ```

2. **Check virtual environment is active**
   (Should see `(venv)` in prompt)

3. **Check dependencies installed**
   ```powershell
   pip list
   ```

4. **Look at error message in console**
   Copy it and check the SETUP_GUIDE.md troubleshooting section

5. **Restart bot**
   - Press `Ctrl+C` to stop
   - Run `python src/bot.py` again

---

## 📁 Project Structure (Final)

```
pro_telegram_bot/
├── .env                          ← YOUR CREDENTIALS (NEVER SHARE!)
├── .gitignore                    ← Prevents .env being uploaded
├── requirements.txt              ← Dependencies to install
├── README.md                     ← Project overview
├── SETUP_GUIDE.md               ← Installation instructions
├── ANTI_SPAM_GUIDE.md           ← Anti-spam features
├── src/
│   ├── bot.py                   ← Main bot entry point
│   ├── database.py              ← Supabase connection & functions
│   └── handlers/
│       ├── __init__.py
│       ├── commands.py          ← /start, /help, /stats
│       ├── moderation.py        ← /warn, /ban, /unmute, /addword
│       └── message_handler.py   ← Anti-spam filter
└── venv/                        ← Virtual environment (auto-created)
```

---

## 🎯 What's Ready

✅ **Bot Features:**
- Persian welcome messages
- User statistics (`/stats`)
- Warning system with auto-mute at 3 warns
- Ban functionality
- Unmute functionality
- Add banned words via `/addword`
- URL/link detection and removal
- 44 banned words configured
- Auto-delete messages after 5-10 seconds
- Admin-only commands
- Event logging

✅ **Database Ready:**
- Supabase tables created
- Default banned words list
- User tracking
- Warning count tracking

✅ **Documentation Complete:**
- Setup guide
- Anti-spam guide
- This checklist

---

## 🚀 You're Ready to Launch!

Just follow the installation steps above and your bot will be live!

**Questions?** Check:
1. SETUP_GUIDE.md (installation & troubleshooting)
2. ANTI_SPAM_GUIDE.md (features & how anti-spam works)
3. README.md (project overview)
