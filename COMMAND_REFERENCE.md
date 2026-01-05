# 🎮 BOT COMMAND REFERENCE CARD

## 👥 USER COMMANDS

### `/start`
**Purpose:** Welcome & initialize user
**Usage:** Type `/start` in group
**Response:** Persian welcome message
**Database:** Saves user to system

**Persian:** شروع بات

---

### `/help`
**Purpose:** Show command menu
**Usage:** Type `/help` in group
**Response:** Complete list of available commands
**Language:** Fully in Persian

**Persian:** راهنما

---

### `/stats`
**Purpose:** Check your warning status
**Usage:** Type `/stats` in group
**Response:** Your warning count & status
**Details:**
- 0 warnings: ✅ شما هیچ اخطاری ندارید!
- 1-2 warnings: ⚠️ Shows remaining warns until mute
- 3+ warnings: 🚫 You are muted!

**Persian:** آمار کاربر

---

## 👮 ADMIN COMMANDS (Visible only to admins)

### `/warn` (Reply to message)
**Purpose:** Warn a user
**Usage:** Reply to user's message, type `/warn`
**Effect:** +1 warning count
**Auto-Action:** At 3 warns → User is muted
**Auto-Delete:** Messages deleted after 5 seconds

**Persian:** اخطار کاربر

**Warning Messages:**
```
1 warn:  ⚠️ 1/3 warns (2 remaining until mute)
2 warns: ⚠️ 2/3 warns (1 remaining until mute)
3 warns: 🚫 MUTED! (can't send messages)
```

---

### `/ban` (Reply to message)
**Purpose:** Permanently ban a user
**Usage:** Reply to user's message, type `/ban`
**Effect:** User removed from group, cannot return
**Auto-Delete:** Messages deleted after 5 seconds
**Confirmation:** Persian message confirms ban

**Persian:** بن کردن کاربر

---

### `/unmute` (Reply to message)
**Purpose:** Remove mute/restrictions
**Usage:** Reply to muted user's message, type `/unmute`
**Effect:** User can send messages again
**Auto-Delete:** Messages deleted after 5 seconds
**Confirmation:** Persian message confirms unmute

**Persian:** باز کردن سکوت

---

### `/addword [word]`
**Purpose:** Add new banned word
**Usage:** `/addword تبلیغ` or `/addword spam`
**Effect:** Word added to filter list
**Response:** Confirmation in Persian
**Auto-Delete:** Messages deleted after 5 seconds
**Updates:** Cache reloaded immediately

**Persian:** اضافه کردن کلمه ممنوع

**Examples:**
```
/addword تبلیغ     → Adds "تبلیغ" to banned list
/addword bitcoin   → Adds "bitcoin" to banned list
/addword spam spam → Adds "spam spam" as phrase
```

**Success:** ✅ کلمه 'تبلیغ' به لیست سیاه اضافه شد.
**Duplicate:** ⚠️ این کلمه قبلاً در لیست سیاه بوده است.

---

## 🤖 AUTOMATIC FILTERING

### Link Detection 🔗
**Detected Patterns:**
- `http://` and `https://` links
- Shortened URLs: `t.me`, `bit.ly`, etc.
- Domain patterns: `.com`, `.ir`, `.net`, `.org`
- `www.` prefix

**Action:**
1. Message deleted immediately
2. Persian warning sent: "🚫 اخطار: ارسال لینک در این گروه مجاز نیست!"
3. Warning auto-deleted after 10 seconds

**Who:** All non-admin users
**Admin:** Can post links freely

---

### Banned Words Filter ⛔
**Total Banned Words:** 44

**Categories:**
- Spam/Advertising (9 words)
- Profanity/Explicit (35 words)

**Spam Words:**
تبلیغ، صیغه، لینک، فروش، خرید، کسب درآمد، کار در خانه، کریپتو، بیت کوین

**Profanity:** (35 words - various levels)

**Action:**
1. Message deleted immediately
2. Persian warning lists deleted words
3. Warning auto-deleted after 10 seconds

**Who:** All non-admin users
**Admin:** Can use any words (no filter)

---

## ⚙️ HOW IT WORKS

### Warning System
```
User sends spam/banned word/link
  ↓
Bot detects it
  ↓
Message deleted
  ↓
Warning sent to user
  ↓
Warning auto-deletes (10 seconds)
```

### Warn Count System
```
/warn → Count: 1/3 (2 remaining)
/warn → Count: 2/3 (1 remaining)
/warn → Count: 3/3 (USER MUTED!)
/unmute → Back to normal
```

### Admin Command Flow
```
Admin types /command (reply to message)
  ↓
Bot verifies admin status
  ↓
Action executed (warn/ban/etc)
  ↓
Confirmation sent in Persian
  ↓
Messages auto-deleted (5 seconds)
```

---

## 📊 QUICK STATS

| Feature | Status |
|---------|--------|
| Total Commands | 7 |
| User Commands | 3 (/start, /help, /stats) |
| Admin Commands | 4 (/warn, /ban, /unmute, /addword) |
| Banned Words | 44 total |
| Auto-Delete Warnings | 10 seconds |
| Auto-Delete Admin Msgs | 5 seconds |
| Warns Until Mute | 3 |
| Language | 100% Persian |

---

## 🔑 KEY FEATURES

✅ **User Management**
- Automatic user registration
- Warning tracking
- Auto-mute at 3 warnings
- Ban/unmute functionality

✅ **Spam Protection**
- URL/link detection
- 44 banned words
- Auto-message deletion
- User warnings

✅ **Admin Controls**
- Warn users
- Ban users
- Unmute users
- Manage banned words

✅ **Professional**
- All Persian interface
- RTL formatting
- Auto-delete spam
- Event logging

---

## 🎯 BEST PRACTICES

### For Regular Users
1. Don't post links (will be deleted)
2. Don't use banned words (will be deleted)
3. Respect group rules (3 warns = mute)
4. Use `/stats` to check your status

### For Admins
1. Keep group clean using `/warn`
2. Ban repeat violators with `/ban`
3. Add custom banned words with `/addword`
4. Monitor logs for patterns

---

## 🆘 COMMON SCENARIOS

### Scenario 1: User posts link
```
User: "Check this https://example.com"
Bot: Deletes message
Bot: Sends warning (🚫 اخطار: ...)
Bot: Deletes warning after 10s
Result: Group stays clean
```

### Scenario 2: User says banned word
```
User: "I want to کون"
Bot: Deletes message
Bot: Sends warning about banned word
Bot: Deletes warning after 10s
Result: Clean conversation
```

### Scenario 3: User gets 3 warnings
```
Admin: /warn (1st time)
Admin: /warn (2nd time)
Admin: /warn (3rd time)
Bot: MUTES user (can't send messages)
Admin: /unmute (to restore)
Result: User learns to behave
```

### Scenario 4: Admin adds banned word
```
Admin: /addword spam123
Bot: ✅ کلمه 'spam123' به لیست سیاه اضافه شد.
Bot: Deletes both messages after 5s
Result: New word automatically filtered
```

---

## 📝 MESSAGE EXAMPLES

### Welcome Message
```
👋 سلام [Username]!

خوش آمدید به گروه ما! 🎉

این بات برای مدیریت و نظارت بر گروه طراحی شده است.
من می‌توانم:
✅ کاربران را اخطار دهم
✅ کاربران مزاحم را مسدود کنم
✅ کلمات ممنوع را فیلتر کنم
✅ آمار و اطلاعات را نمایش دهم

برای دیدن دستورات بیشتر، /help را بزنید.
```

### Link Warning
```
🚫 اخطار:

ارسال لینک در این گروه مجاز نیست!

⛔ لطفاً از ارسال لینک‌ها خودداری کنید.
```

### Banned Word Warning
```
🚫 اخطار:

ارسال کلمات ممنوعه در این گروه مجاز نیست!

⛔ کلمات حذف‌شده: [word1، word2، ...]

⚠️ لطفاً رعایت قوانین گروه کنید.
```

### Warn Message
```
⚠️ اخطار برای @username

📊 اخطار: 1/3
⏰ 2 اخطار باقی‌مانده تا مسدود شدن
```

---

## 🔐 SECURITY NOTES

✅ Admin commands only work for group admins
✅ Regular users see only general commands
✅ All actions logged to console
✅ Database tracks all events
✅ Credentials stored safely in .env

---

## 📖 Need More Help?

- **QUICKSTART.md** - 5-minute setup
- **SETUP_GUIDE.md** - Installation & troubleshooting
- **ANTI_SPAM_GUIDE.md** - Detailed filter info
- **VERIFICATION_REPORT.md** - Code details

---

**Version:** 1.0
**Language:** Persian (فارسی)
**Status:** Production Ready
**Last Updated:** 2025-12-29

Keep this card handy! 📋
