"""
Moderation handlers for group administration (Persian/Farsi)
"""

import logging
import asyncio
from telegram import Update, ChatMember, ChatPermissions
from telegram.ext import ContextTypes
from src.database import db

logger = logging.getLogger(__name__)

# 🔴 GLOBAL OWNER ID
OWNER_ID = 2117254740

async def delete_later(bot, chat_id, message_id, delay):
    """Wait for 'delay' seconds, then delete the message"""
    try:
        await asyncio.sleep(delay)
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception:
        pass

async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Check if the user is a group administrator OR the Bot Owner"""
    if not update.message or not update.effective_user:
        return False
    
    # 🟢 GOD MODE: Owner can always run commands
    if update.effective_user.id == OWNER_ID:
        return True

    try:
        # Get user status in the chat
        user_status = await update.message.chat.get_member(update.effective_user.id)
        
        # Check if user is admin or owner
        admin_statuses = [ChatMember.ADMINISTRATOR, ChatMember.OWNER]
        
        if hasattr(ChatMember, 'CREATOR'):
            admin_statuses.append(ChatMember.CREATOR)
        
        return user_status.status in admin_statuses
    except Exception as e:
        logger.error(f"Error checking admin: {e}")
        return False


async def delete_messages(context: ContextTypes.DEFAULT_TYPE, chat_id: int, message_id: int, admin_message_id: int = None):
    """Delete bot and admin messages after 5 seconds"""
    try:
        await context.bot.delete_message(chat_id, message_id)
        if admin_message_id:
            await context.bot.delete_message(chat_id, admin_message_id)
    except Exception as e:
        logger.warning(f"Error deleting message: {e}")


async def warn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /warn command"""
    if not update.message or not update.effective_user: return
    if not await is_admin(update, context): return

    try: await update.message.delete()
    except Exception: pass
    
    if not update.message.reply_to_message or not update.message.reply_to_message.from_user:
        msg = await context.bot.send_message(chat_id=update.message.chat_id, text="⚠️ لطفاً به پیام کاربر پاسخ دهید.")
        asyncio.create_task(delete_later(context.bot, update.message.chat_id, msg.message_id, 3))
        return
    
    target_user = update.message.reply_to_message.from_user
    new_warn_count = db.add_warn(target_user.id)
    
    if new_warn_count is None: return

    if new_warn_count >= 3:
        try:
            await context.bot.restrict_chat_member(
                chat_id=update.message.chat_id,
                user_id=target_user.id,
                permissions=ChatPermissions(can_send_messages=False)
            )
            warning_msg = f"🚫 کاربر {target_user.mention_html()} به دلیل دریافت ۳ اخطار مسدود شد!"
        except Exception:
            warning_msg = f"🚫 اخطار سوم برای {target_user.mention_html()} (خطا در مسدود سازی)"
    else:
        warning_msg = f"⚠️ اخطار برای {target_user.mention_html()}\n📊 تعداد: {new_warn_count}/3"
    
    response = await context.bot.send_message(chat_id=update.message.chat_id, text=warning_msg, parse_mode="HTML")
    asyncio.create_task(delete_later(context.bot, update.message.chat_id, response.message_id, 10))


async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /ban command"""
    if not update.message or not update.effective_user: return
    if not await is_admin(update, context): return

    try: await update.message.delete()
    except Exception: pass
    
    if not update.message.reply_to_message:
        msg = await context.bot.send_message(chat_id=update.message.chat_id, text="⚠️ لطفاً به پیام کاربر پاسخ دهید.")
        asyncio.create_task(delete_later(context.bot, update.message.chat_id, msg.message_id, 3))
        return
    
    target_user = update.message.reply_to_message.from_user
    
    try:
        await context.bot.ban_chat_member(chat_id=update.message.chat_id, user_id=target_user.id)
        ban_msg = f"🚫 کاربر {target_user.mention_html()} از گروه اخراج شد."
    except Exception as e:
        ban_msg = "❌ خطا در بن کردن کاربر."
    
    response = await context.bot.send_message(chat_id=update.message.chat_id, text=ban_msg, parse_mode="HTML")
    asyncio.create_task(delete_later(context.bot, update.message.chat_id, response.message_id, 5))


async def unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /unmute command - Via Reply, ID, or @Username"""
    if not update.message or not update.effective_user: return
    if not await is_admin(update, context): return

    try: await update.message.delete()
    except Exception: pass
    
    target_user_id = None
    target_name = "کاربر"

    if update.message.reply_to_message:
        target_user_id = update.message.reply_to_message.from_user.id
        target_name = update.message.reply_to_message.from_user.mention_html()
    elif context.args:
        arg = context.args[0]
        if arg.startswith("@") or not arg.isdigit():
            found_id = db.get_user_id_by_username(arg)
            if found_id:
                target_user_id = found_id
                target_name = f"{arg}"
            else:
                msg = await context.bot.send_message(chat_id=update.message.chat_id, text=f"❌ کاربر {arg} یافت نشد.")
                asyncio.create_task(delete_later(context.bot, update.message.chat_id, msg.message_id, 5))
                return
        else:
            try:
                target_user_id = int(arg)
                target_name = f"<a href='tg://user?id={target_user_id}'>{target_user_id}</a>"
            except ValueError: pass

    if not target_user_id:
        msg = await context.bot.send_message(chat_id=update.message.chat_id, text="⚠️ لطفا ریپلای کنید یا آیدی/نام کاربری وارد کنید.", parse_mode="HTML")
        asyncio.create_task(delete_later(context.bot, update.message.chat_id, msg.message_id, 5))
        return
    
    try:
        await context.bot.unban_chat_member(chat_id=update.message.chat_id, user_id=target_user_id)
        db.reset_warns(target_user_id)
        try:
            await context.bot.restrict_chat_member(
                chat_id=update.message.chat_id,
                user_id=target_user_id,
                permissions=ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_polls=True, can_add_web_page_previews=True)
            )
        except Exception: pass
        msg_text = f"✅ محدودیت‌های {target_name} برداشته شد."
    except Exception as e:
        msg_text = f"❌ خطا: {e}"
    
    response = await context.bot.send_message(chat_id=update.message.chat_id, text=msg_text, parse_mode="HTML")
    asyncio.create_task(delete_later(context.bot, update.message.chat_id, response.message_id, 5))


async def addword(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /addword command"""
    if not update.message or not update.effective_user: return
    if not await is_admin(update, context): return
    
    try: await update.message.delete()
    except Exception: pass

    if not context.args or len(context.args) == 0:
        msg = await context.bot.send_message(chat_id=update.message.chat_id, text="⚠️ لطفا کلمه را وارد کنید.")
        asyncio.create_task(delete_later(context.bot, update.message.chat_id, msg.message_id, 2))
        return
    
    word = " ".join(context.args).strip()
    result = db.add_banned_word(word)
    
    if result is None: text = f"⚠️ کلمه '{word}' قبلاً وجود داشت."
    else: text = f"✅ کلمه '{word}' اضافه شد."
    
    response = await context.bot.send_message(chat_id=update.message.chat_id, text=text)
    asyncio.create_task(delete_later(context.bot, update.message.chat_id, response.message_id, 2))


async def authorize(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """(Owner Only) Authorize the current group to use the bot"""
    if not update.message or not update.effective_user: return
    
    # Check GLOBAL Owner ID
    if update.effective_user.id != OWNER_ID:
        return 

    chat_id = update.message.chat_id
    chat_title = update.message.chat.title or "Unknown Group"
    
    if db.add_allowed_group(chat_id, chat_title):
        await update.message.reply_text("✅ این گروه با موفقیت فعال شد (Licensed).")
    else:
        await update.message.reply_text("⚠️ این گروه قبلاً فعال شده است.")
    
    try: await update.message.delete() 
    except: pass