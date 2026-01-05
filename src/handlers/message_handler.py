"""
Message handlers for processing group messages (Persian/Farsi)
Portfolio Version - Manual Approval Only
"""

import logging
import re
import asyncio
from telegram import Update, ChatMember, ChatPermissions, MessageEntity
from telegram.ext import ContextTypes
from src.database import db

logger = logging.getLogger(__name__)

# MEMORY for Approval System
PENDING_APPROVALS = {}

# ==================== HELPER FUNCTIONS ====================

async def delete_later(bot, chat_id, message_id, delay):
    """Wait for 'delay' seconds, then delete the message"""
    try:
        await asyncio.sleep(delay)
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception:
        pass

async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    if not update.message or not update.effective_user:
        return False
    try:
        user_status = await update.message.chat.get_member(update.effective_user.id)
        admin_statuses = [ChatMember.ADMINISTRATOR, ChatMember.OWNER]
        if hasattr(ChatMember, 'CREATOR'):
            admin_statuses.append(ChatMember.CREATOR)
        return user_status.status in admin_statuses
    except Exception:
        return False

async def log_spam_event(user_id: int, username: str, spam_type: str, content: str, chat_id: int):
    try:
        logger.warning(f"🚨 Spam: {spam_type} | User: {username}({user_id}) | Content: {content}")
    except Exception:
        pass

async def handle_punishment(update: Update, context: ContextTypes.DEFAULT_TYPE, user, reason: str):
    new_warn_count = db.add_warn(user.id)
    user_mention = user.mention_html()
    
    if new_warn_count >= 3:
        try:
            await context.bot.ban_chat_member(chat_id=update.message.chat_id, user_id=user.id)
            msg_text = f"🚫 کاربر {user_mention} به دلیل {reason} و دریافت ۳ اخطار **مسدود شد**!"
        except Exception:
            msg_text = f"🚫 اخطار سوم برای {user_mention} (ربات دسترسی بن ندارد)."
    else:
        msg_text = f"🚫 {user_mention} عزیز، {reason} مجاز نیست.\n⚠️ اخطار: {new_warn_count}/3"

    warning = await context.bot.send_message(chat_id=update.message.chat_id, text=msg_text, parse_mode="HTML")
    asyncio.create_task(delete_later(context.bot, update.message.chat_id, warning.message_id, 5))

# ==================== LOGIC: TEXT CLEANING ====================

def normalize_text(text: str) -> str:
    if not text: return ""
    # Nuclear Cleaning
    clean = re.sub(r'[^\w\d\u0600-\u06FF]', '', text)
    clean = clean.replace('_', '')
    clean = re.sub(r'(.)\1+', r'\1', clean)
    return clean.lower()

def has_link(message) -> bool:
    entities = message.entities or []
    caption_entities = message.caption_entities or []
    all_entities = list(entities) + list(caption_entities)
    for entity in all_entities:
        if entity.type in [MessageEntity.URL, MessageEntity.TEXT_LINK]:
            return True

    text_content = message.text or message.caption or ""
    text_lower = text_content.lower()
    
    url_keywords = ['http://', 'https://', 'www.', '.com', '.ir', '.net', '.org', 't.me', 'bit.ly']
    for keyword in url_keywords:
        if keyword in text_lower: return True

    # Advanced Skeleton
    skeleton = re.sub(r'[^a-z]+', '', text_lower)
    skeleton_clean = re.sub(r'(.)\1+', r'\1', skeleton)
    
    extensions = ['com', 'ir', 'net', 'org', 'xyz', 'tk', 'info', 'io', 'me', 'site']
    common_sites = ['google', 'youtube', 'instagram', 'telegram', 'whatsapp', 'sex', 'porn', 'xxx']
    prefixes = ['http', 'https', 'www', 'tme']

    for site in common_sites:
        for ext in extensions:
            if site + ext in skeleton_clean: return True

    for p in prefixes:
        if p in skeleton_clean: return True

    has_symbols = bool(re.search(r'[\./,\\_]', text_lower))
    if has_symbols:
        for ext in extensions:
            if skeleton_clean.endswith(ext):
                if len(skeleton_clean) > len(ext) + 2:
                    return True
    return False

# ==================== HANDLER 1: APPROVAL LOGIC ====================

async def handle_approval(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 🔴 REPLACE WITH YOUR ID FOR THE NEW BOT
    OWNER_ID = 2117254740 
    
    if update.effective_user.id != OWNER_ID: return
    if not update.message.reply_to_message: return

    target_msg_id = update.message.reply_to_message.message_id
    data = PENDING_APPROVALS.get(target_msg_id)

    if not data:
        await update.message.reply_text("⚠️ پیام یافت نشد.")
        return

    group_id = data['chat_id']
    user_id = data['user_id']
    command = update.message.text

    try:
        if command == "تایید":
            await update.message.reply_to_message.copy(
                chat_id=group_id,
                caption=f"✅ <b>تایید شد</b>\nتوسط مدیر گروه.",
                parse_mode="HTML"
            )
            await update.message.reply_text("✅ ارسال شد.")
            
        elif command == "رد":
            try:
                member = await context.bot.get_chat_member(group_id, user_id)
                user_mention = member.user.mention_html()
            except:
                user_mention = "کاربر"
            
            reject_msg = f"❌ مدیا ارسالی توسط {user_mention} **تایید نشد**."
            msg = await context.bot.send_message(chat_id=group_id, text=reject_msg, parse_mode="HTML")
            asyncio.create_task(delete_later(context.bot, group_id, msg.message_id, 10))
            await update.message.reply_text("❌ رد شد.")

        del PENDING_APPROVALS[target_msg_id]
    except Exception as e:
        logger.error(f"Approval error: {e}")

# ==================== HANDLER 2: MEDIA (MANUAL ONLY) ====================

async def check_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles Photos/Videos/GIFs/Stickers.
    NO AI -> Direct Forward to Admin.
    """
    if not update.message or not update.effective_user: return
    if await is_admin(update, context): return

    try:
        # 🔴 REPLACE WITH YOUR ID FOR THE NEW BOT
        OWNER_ID = 2117254740
        
        # A. Forward FIRST
        try:
            forwarded_msg = await update.message.forward(chat_id=OWNER_ID)
            PENDING_APPROVALS[forwarded_msg.message_id] = {
                'chat_id': update.message.chat_id,
                'user_id': update.effective_user.id
            }
            await context.bot.send_message(
                chat_id=OWNER_ID, 
                text=f"📩 <b>مدیا برای تایید</b>\nکاربر: {update.effective_user.mention_html()}\nگروه: {update.message.chat.title}\n\n✅ تایید / ❌ رد", 
                parse_mode="HTML"
            )
        except Exception: 
            pass 

        # B. Delete SECOND
        await update.message.delete()

        msg_text = f"🔒 {update.effective_user.mention_html()} عزیز، فایل شما برای بررسی ارسال شد."
        warning = await context.bot.send_message(chat_id=update.message.chat_id, text=msg_text, parse_mode="HTML")
        asyncio.create_task(delete_later(context.bot, update.message.chat_id, warning.message_id, 5))
        
    except Exception as e:
        logger.error(f"Media handler error: {e}")

# ==================== HANDLER 3: TEXT ====================

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.effective_user: return
    
    user = update.effective_user
    message = update.message
    db.initialize_user(user.id, user.username or "Unknown")
    
    if await is_admin(update, context): return

    message_text = message.text or message.caption or ""
    if not message_text: return 
    message_text_lower = message_text.lower()
    
    if has_link(message):
        try:
            await message.delete()
            await handle_punishment(update, context, user, "ارسال لینک")
            await log_spam_event(user.id, user.username or "Unknown", "link", message_text[:100], message.chat_id)
            return
        except Exception: pass
    
    banned_words = db.get_banned_words()
    if banned_words:
        cleaned_message = normalize_text(message_text_lower)
        found_banned = False
        found_word = ""
        for word in banned_words:
            if word in message_text_lower:
                found_banned = True; found_word = word; break
            word_clean = normalize_text(word)
            if word_clean and word_clean in cleaned_message:
                found_banned = True; found_word = word; break
        
        if found_banned:
            try:
                await message.delete()
                await handle_punishment(update, context, user, "ارسال کلمات نامناسب")
                await log_spam_event(user.id, user.username or "Unknown", "banned_word", found_word, message.chat.id)
            except Exception: pass