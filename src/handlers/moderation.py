"""
Moderation handlers for group administration (Persian/Farsi)
"""

import logging
import asyncio
from telegram import Update, ChatMember, ChatPermissions
from telegram.ext import ContextTypes
from src.database import db

logger = logging.getLogger(__name__)

async def delete_later(bot, chat_id, message_id, delay):
    """Wait for 'delay' seconds, then delete the message"""
    try:
        await asyncio.sleep(delay)
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception:
        pass

# 🔴 2. SET YOUR OWNER ID HERE
OWNER_ID = 2117254740

async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Check if the user is a group administrator"""
    if not update.message or not update.effective_user:
        return False
    
    try:
        # Get user status in the chat
        user_status = await update.message.chat.get_member(update.effective_user.id)
        
        # Check if user is admin or owner (CREATOR is deprecated, use OWNER)
        # We check for both to be safe
        admin_statuses = [ChatMember.ADMINISTRATOR, ChatMember.OWNER]
        
        # Fallback for older versions that might still use CREATOR
        if hasattr(ChatMember, 'CREATOR'):
            admin_statuses.append(ChatMember.CREATOR)
        
        return user_status.status in admin_statuses
    except Exception as e:
        logger.error(f"خطا در بررسی دسترسی ادمین: {e}")
        return False


async def delete_messages(context: ContextTypes.DEFAULT_TYPE, chat_id: int, message_id: int, admin_message_id: int = None):
    """Delete bot and admin messages after 5 seconds"""
    try:
        # Delete bot's response message
        await context.bot.delete_message(chat_id, message_id)
        
        # Delete admin's command message if provided
        if admin_message_id:
            await context.bot.delete_message(chat_id, admin_message_id)
    except Exception as e:
        logger.warning(f"خطا در حذف پیام: {e}")


async def warn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /warn command - Warn a user (Flash Mode)"""
    if not update.message or not update.effective_user:
        return
    
    # Check admin permissions
    if not await is_admin(update, context):
        return

    # 1. Delete Admin's Command IMMEDIATELY
    try:
        await update.message.delete()
    except Exception:
        pass
    
    # Check if replying to a message
    if not update.message.reply_to_message or not update.message.reply_to_message.from_user:
        # Send error, delete after 3s
        msg = await context.bot.send_message(chat_id=update.message.chat_id, text="⚠️ لطفاً به پیام کاربر پاسخ دهید.")
        context.job_queue.run_once(lambda ctx: ctx.bot.delete_message(update.message.chat_id, msg.message_id), when=3)
        return
    
    target_user = update.message.reply_to_message.from_user
    
    # Add warning to database
    new_warn_count = db.add_warn(target_user.id)
    
    if new_warn_count is None:
        return

    # Prepare Message
    if new_warn_count >= 3:
        # Mute the user
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
    
    # 2. Send Warning
    response = await context.bot.send_message(
        chat_id=update.message.chat_id,
        text=warning_msg,
        parse_mode="HTML"
    )
    
    # Delete after 10 seconds
    asyncio.create_task(delete_later(context.bot, update.message.chat_id, response.message_id, 10))


async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /ban command - Ban a user (Flash Mode)"""
    if not update.message or not update.effective_user:
        return
    
    if not await is_admin(update, context):
        return

    # 1. Delete Admin's Command
    try:
        await update.message.delete()
    except Exception:
        pass
    
    if not update.message.reply_to_message:
        msg = await context.bot.send_message(chat_id=update.message.chat_id, text="⚠️ لطفاً به پیام کاربر پاسخ دهید.")
        context.job_queue.run_once(lambda ctx: ctx.bot.delete_message(update.message.chat_id, msg.message_id), when=3)
        return
    
    target_user = update.message.reply_to_message.from_user
    
    try:
        await context.bot.ban_chat_member(chat_id=update.message.chat_id, user_id=target_user.id)
        ban_msg = f"🚫 کاربر {target_user.mention_html()} از گروه اخراج شد."
    except Exception as e:
        ban_msg = "❌ خطا در بن کردن کاربر."
    
    # 2. Send Confirmation
    response = await context.bot.send_message(chat_id=update.message.chat_id, text=ban_msg, parse_mode="HTML")
    
    # Delete after 5 seconds
    asyncio.create_task(delete_later(context.bot, update.message.chat_id, response.message_id, 5))

async def unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /unmute command - Via Reply, ID, or @Username"""
    if not update.message or not update.effective_user:
        return
    
    if not await is_admin(update, context):
        return

    # 1. Delete Admin Command
    try:
        await update.message.delete()
    except Exception:
        pass
    
    target_user_id = None
    target_name = "کاربر"

    # CASE A: Reply
    if update.message.reply_to_message:
        target_user_id = update.message.reply_to_message.from_user.id
        target_name = update.message.reply_to_message.from_user.mention_html()
    
    # CASE B: Arguments (ID or Username)
    elif context.args:
        arg = context.args[0]
        
        # Check if it looks like a username (Starts with @ or contains letters)
        if arg.startswith("@") or not arg.isdigit():
            # Look up in Database
            found_id = db.get_user_id_by_username(arg)
            if found_id:
                target_user_id = found_id
                target_name = f"{arg}"
            else:
                msg = await context.bot.send_message(
                    chat_id=update.message.chat_id,
                    text=f"❌ کاربر {arg} در حافظه ربات پیدا نشد.\n(فقط کاربرانی که قبلاً پیام داده‌اند در حافظه هستند)"
                )
                asyncio.create_task(delete_later(context.bot, update.message.chat_id, msg.message_id, 5))
                return
        else:
            # Assume it's a numeric ID
            try:
                target_user_id = int(arg)
                target_name = f"<a href='tg://user?id={target_user_id}'>{target_user_id}</a>"
            except ValueError:
                pass

    # If still no user found
    if not target_user_id:
        msg = await context.bot.send_message(
            chat_id=update.message.chat_id, 
            text="⚠️ لطفاً روی پیام کاربر ریپلای کنید یا نام کاربری/آیدی او را وارد کنید.\nمثال: /unmute @username",
            parse_mode="HTML"
        )
        asyncio.create_task(delete_later(context.bot, update.message.chat_id, msg.message_id, 5))
        return
    
    # Perform Unban
    try:
        # A. Unban
        await context.bot.unban_chat_member(chat_id=update.message.chat_id, user_id=target_user_id)
        
        # B. Reset warnings
        db.reset_warns(target_user_id)
        
        # C. Lift Restrictions
        try:
            await context.bot.restrict_chat_member(
                chat_id=update.message.chat_id,
                user_id=target_user_id,
                permissions=ChatPermissions(
                    can_send_messages=True, can_send_media_messages=True,
                    can_send_polls=True, can_add_web_page_previews=True
                )
            )
        except Exception:
            pass

        msg_text = f"✅ محدودیت‌های {target_name} برداشته شد."
    except Exception as e:
        msg_text = f"❌ خطا در بخشش کاربر: {e}"
    
    # Send Confirmation
    response = await context.bot.send_message(chat_id=update.message.chat_id, text=msg_text, parse_mode="HTML")
    asyncio.create_task(delete_later(context.bot, update.message.chat_id, response.message_id, 5))


async def addword(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /addword command - Add a banned word (Flash Mode)"""
    if not update.message or not update.effective_user:
        return
    
    # Check admin permissions
    if not await is_admin(update, context):
        return
    
    # 1. Delete the command message IMMEDIATELY
    try:
        await update.message.delete()
    except Exception:
        pass

    # Check if word is provided
    if not context.args or len(context.args) == 0:
        msg = await context.bot.send_message(
            chat_id=update.message.chat_id,
            text="⚠️ لطفاً کلمه را وارد کنید. (مثال: /addword تبلیغ)"
        )
        # Delete after 2 seconds
        asyncio.create_task(delete_later(context.bot, update.message.chat_id, response.message_id, 2))
    
    word = " ".join(context.args).strip()
    
    # Add to DB
    result = db.add_banned_word(word)
    
    if result is None:
        text = f"⚠️ کلمه '{word}' قبلاً وجود داشت."
    else:
        text = f"✅ کلمه '{word}' اضافه شد."
        logger.info(f"کلمه '{word}' توسط {update.effective_user.id} اضافه شد")
    
    # 2. Send Confirmation
    response = await context.bot.send_message(
        chat_id=update.message.chat_id,
        text=text
    )
    
    # Flash Delete (2 seconds)
    asyncio.create_task(delete_later(context.bot, update.message.chat_id, response.message_id, 2))