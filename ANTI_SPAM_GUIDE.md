# 🛡️ Professional Anti-Spam Filter Guide

## Overview
The bot includes a comprehensive anti-spam system that:
- Detects and removes messages containing URLs/links
- Filters banned Persian words
- Auto-deletes warnings after 10 seconds
- Logs all spam events
- Skips admin users automatically

---

## ✨ Features Implemented

### 1. **URL/Link Detection**
- Detects `http://`, `https://` links
- Detects shortened URLs (`t.me`, `bit.ly`, etc.)
- Detects common domain patterns (`.com`, `.ir`, `.net`, `.org`)
- Skips admins (they can post links)

**Example:**
```
User posts: "Check this link https://example.com"
Bot: Deletes message + sends warning + deletes warning after 10 seconds
```

### 2. **Banned Words Filter**
- Pulls from Supabase `banned_words` table
- Caches words in memory for fast checking
- Default Persian spam words included:
  - تبلیغ (advertising)
  - صیغه (marriage proposal scam)
  - لینک (link)
  - فروش (selling)
  - خرید (buying)
  - کسب درآمد (earning money - MLM/scam)
  - کار در خانه (work from home - scam)
  - کریپتو (crypto)
  - بیت کوین (bitcoin)

**Example:**
```
User posts: "فروش محصولات بهتر"
Bot: Deletes message + warns about banned words + deletes warning after 10 seconds
```

### 3. **Auto-Delete Warnings**
- Uses `JobQueue` to schedule deletion
- Warning messages auto-delete after 10 seconds
- Keeps group chat clean and organized
- Admin messages also auto-delete after 5 seconds

### 4. **Event Logging**
- All spam events logged with details:
  - User ID and username
  - Type of spam (link/banned_word)
  - Content that triggered filter
  - Chat ID
  - Timestamp

### 5. **Admin Bypass**
- Admins can post links and banned words
- Detection checks admin status before filtering
- No spam warnings for administrators

---

## 🛠️ Database Integration

### Tables Required

**banned_words table:**
```sql
CREATE TABLE banned_words (
  id BIGSERIAL PRIMARY KEY,
  word TEXT UNIQUE NOT NULL,
  added_at TIMESTAMP DEFAULT NOW()
);
```

### Functions Used

**`db.get_banned_words()`**
- Returns cached list of banned words
- Auto-loads from database if cache empty
- Updates cache when new words added

**`db.initialize_default_banned_words()`**
- Initializes database with default Persian spam words
- Only inserts if table is empty
- Call in bot startup (optional)

**`db.add_banned_word(word)`**
- Adds new word to banned list
- Updates cache immediately
- Prevents duplicates

**`db.remove_banned_word(word)`**
- Removes word from banned list
- Updates cache immediately

---

## 📋 Persian Warning Messages

All warnings use professional Persian formatting:

### Link Warning (RTL)
```
🚫 اخطار:

ارسال لینک در این گروه مجاز نیست!

⛔ لطفاً از ارسال لینک‌ها خودداری کنید.
```

### Banned Word Warning (RTL)
```
🚫 اخطار:

ارسال کلمات ممنوعه در این گروه مجاز نیست!

⛔ کلمات حذف‌شده: [word1، word2، ...]

⚠️ لطفاً رعایت قوانین گروه کنید.
```

### Formatting Details
- ✅ All messages use `parse_mode="HTML"`
- ✅ Start with Persian emoji or Persian text (RTL compliance)
- ✅ Bold text using `<b>...</b>` tags
- ✅ Code formatting for banned words: `<code>...</code>`
- ✅ No English text at message start

---

## 🔧 Configuration

### Add New Banned Words via Bot

Admin users can add banned words using:
```
/addword تبلیغ
/addword لینک
/addword فروش
```

Response: `✅ کلمه 'تبلیغ' به لیست سیاه اضافه شد.`

### Initialize Default Words

In `src/bot.py`, after creating the bot instance:
```python
# Initialize default banned words (optional, one-time setup)
db.initialize_default_banned_words()
```

---

## 🚀 How It Works - Flow Diagram

```
Message Received
    ↓
Is User Admin? → YES → Allow message (no filter)
    ↓ NO
Contains URL? → YES → Delete + Warn + Log → Schedule delete warning (10s)
    ↓ NO
Contains Banned Word? → YES → Delete + Warn + Log → Schedule delete warning (10s)
    ↓ NO
Allow Message
```

---

## 📊 Logging

All spam events logged in console with format:
```
WARNING:src.handlers.message_handler:🔗 لینک توسط 123456789 (@username) حذف شد. گروه: -1001234567890
```

---

## 🔐 Admin Commands for Moderation

- `/warn @user` - Warn user (3 warns = mute)
- `/ban @user` - Permanently ban
- `/unmute @user` - Remove mute
- `/addword word` - Add to banned list

All admin commands:
- ✅ Admin-only visibility
- ✅ Auto-delete after 5 seconds
- ✅ Persian messages
- ✅ Logged to console

---

## 💡 Performance Notes

- **Banned words cached in memory** - Fast checking, no DB calls per message
- **Cache reloaded** when:
  - Bot starts
  - New word added via `/addword`
  - Explicitly called via `db.load_banned_words_cache()`
- **JobQueue** handles auto-deletion efficiently

---

## ✅ Testing Checklist

- [ ] Post a link (e.g., `https://example.com`) as regular user
- [ ] Post a banned word (e.g., `تبلیغ`) as regular user
- [ ] Verify message deleted immediately
- [ ] Verify warning appears
- [ ] Verify warning auto-deletes after 10 seconds
- [ ] Post link as admin - should work fine
- [ ] Use `/addword newword` - should add to filter
- [ ] Verify logs show spam events

---

## 🎯 Next Steps

When credentials are provided:
1. Run: `python src/bot.py`
2. Test in your group
3. Adjust banned words as needed via `/addword`
4. Monitor logs for patterns

Happy moderation! 🛡️
