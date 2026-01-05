"""
Command handlers for the Telegram bot (Persian/Farsi)
"""

import logging
import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from src.database import db

logger = logging.getLogger(__name__)

# Helper for Flash Messages
async def delete_later(bot, chat_id, message_id, delay):
    try:
        await asyncio.sleep(delay)
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception:
        pass

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command - Detailed Welcome Message"""
    try:
        if not update.message or not update.effective_user:
            return
        
        user = update.effective_user
        
        # Initialize user in database
        db.initialize_user(user.id, user.username or "Unknown")
        
        # 🟢 NEW DETAILED WELCOME MESSAGE
        welcome_message = f"""👋 سلام {user.first_name} عزیز!

🤖 <b>به ربات محافظ هوشمند گروه خوش آمدید!</b>

این ربات برای حفظ امنیت و کیفیت گروه، قوانین زیر را به صورت خودکار اجرا می‌کند:

🛡️ <b>۱. فیلتر پیشرفته لینک‌ها:</b>
⛔ ارسال هرگونه لینک ممنوع است.
⛔ ربات حتی لینک‌های مخفی و بهم‌ریخته (مثل w w w . g o o g l e) را شناسایی و حذف می‌کند.

🗣️ <b>۲. فیلتر کلمات نامناسب:</b>
⛔ ارسال کلمات رکیک و ممنوعه مجاز نیست.
⛔ ربات کلماتی که با فاصله، نقطه یا ایموجی مخفی شده‌اند (مثل ت.ب.ل.ی.غ) را تشخیص می‌دهد.

📷 <b>۳. تایید محتوای رسانه‌ای:</b>
🔒 ارسال <b>عکس، ویدیو، گیف و استیکر</b> نیازمند تایید است.
📩 فایل‌های شما ابتدا حذف شده و برای مدیر ارسال می‌شوند. فقط در صورت <b>تایید مدیر</b> در گروه نمایش داده می‌شوند.

⚖️ <b>۴. سیستم جریمه:</b>
⚠️ هر بار تخلف = ۱ اخطار
🚫 دریافت ۳ اخطار = <b>مسدود شدن (Ban)</b> از گروه

برای مشاهده وضعیت اخطارهای خود دستور /stats را بزنید."""
        
        # Send message
        response = await update.message.reply_text(welcome_message, parse_mode="HTML")
        
        # Auto-delete after 30 seconds if sent in a group (keep chat clean)
        if update.message.chat.type != 'private':
            asyncio.create_task(delete_later(context.bot, update.message.chat_id, response.message_id, 30))
            # Delete user's command
            asyncio.create_task(delete_later(context.bot, update.message.chat_id, update.message.message_id, 30))
            
    except Exception as e:
        logger.error(f"Error in /start command: {e}")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    try:
        if not update.message:
            return
        
        help_text = """📖 <b>راهنمای دستورات:</b>

👥 <b>کاربران عادی:</b>
/start - مشاهده قوانین و قابلیت‌های ربات
/stats - مشاهده تعداد اخطارها و وضعیت شما

⚙️ <b>مدیران (فقط ادمین):</b>
/warn - اخطار دستی به کاربر (ریپلای)
/ban - مسدود کردن کاربر (ریپلای)
/unmute - بخشش و رفع مسدودیت (ریپلای یا آیدی)
/addword [کلمه] - افزودن کلمه به لیست سیاه

✅ <b>تایید مدیا:</b>
برای تایید عکس/فیلم کاربران، در چت خصوصی روی آن ریپلای کنید: <b>تایید</b>
برای رد کردن: <b>رد</b>"""
        
        response = await update.message.reply_text(help_text, parse_mode="HTML")
        
        if update.message.chat.type != 'private':
            asyncio.create_task(delete_later(context.bot, update.message.chat_id, response.message_id, 20))
            asyncio.create_task(delete_later(context.bot, update.message.chat_id, update.message.message_id, 20))
            
    except Exception as e:
        logger.error(f"Error in /help command: {e}")


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /stats command"""
    try:
        if not update.message or not update.effective_user:
            return
        
        user = update.effective_user
        user_stats = db.get_user_stats(user.id)
        
        if not user_stats:
            # If user not found, init them and say 0 warnings
            db.initialize_user(user.id, user.username or "Unknown")
            warn_count = 0
        else:
            warn_count = user_stats.get("warn_count", 0)
            
        if warn_count == 0:
            status = "✅ وضعیت: عالی (بدون اخطار)"
        elif warn_count < 3:
            remaining = 3 - warn_count
            status = f"⚠️ وضعیت: هشدار ({remaining} اخطار تا مسدودیت)"
        else:
            status = "🚫 وضعیت: مسدود شده"
        
        response = f"""📊 <b>آمار کاربر:</b>

👤 نام: {user.first_name}
🆔 شناسه: <code>{user.id}</code>
⚠️ تعداد اخطار: {warn_count} از ۳
{status}"""
        
        msg = await update.message.reply_text(response, parse_mode="HTML")
        
        if update.message.chat.type != 'private':
            asyncio.create_task(delete_later(context.bot, update.message.chat_id, msg.message_id, 15))
            asyncio.create_task(delete_later(context.bot, update.message.chat_id, update.message.message_id, 15))
            
    except Exception as e:
        logger.error(f"Error in /stats command: {e}")