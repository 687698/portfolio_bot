"""
Main Telegram Bot Entry Point
Persian Community Management Bot for large group administration
"""

import os
import logging
import asyncio
from dotenv import load_dotenv
from telegram import Update, BotCommand, BotCommandScopeAllChatAdministrators
from telegram.request import HTTPXRequest
from telegram.ext import Application, ContextTypes, CommandHandler, MessageHandler, filters

# Load environment variables (from .env if it exists locally)
# On Railway, environment variables are set directly in the dashboard
load_dotenv(override=False)

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=os.getenv("LOG_LEVEL", "INFO")
)
logger = logging.getLogger(__name__)


async def setup_commands(app):
    """Setup bot commands with proper scopes"""
    # Commands for all users
    general_commands = [
        BotCommand("start", "🏠 شروع بات"),
        BotCommand("help", "📖 راهنما"),
        BotCommand("stats", "📊 آمار کاربر"),
    ]
    
    # Admin-only commands
    admin_commands = [
        BotCommand("warn", "⚠️ اخطار کاربر"),
        BotCommand("ban", "🚫 بن کردن کاربر"),
        BotCommand("unmute", "🔊 باز کردن سکوت"),
        BotCommand("addword", "📝 اضافه کردن کلمه ممنوع"),
    ]
    
    try:
        # Set general commands for all users
        await app.bot.set_my_commands(general_commands)
        
        # Set admin commands only for administrators
        await app.bot.set_my_commands(
            admin_commands,
            scope=BotCommandScopeAllChatAdministrators()
        )
        
        logger.info("✅ Bot commands configured successfully")
    except Exception as e:
        logger.error(f"Error setting commands: {e}")


async def setup_application():
    """Setup and return the application (non-blocking setup)"""
    # Get token from environment
    token = os.getenv("TELEGRAM_TOKEN")
    
    if not token:
        # Debug: show all environment variables
        logger.error("Missing TELEGRAM_TOKEN. Available env variables:")
        for key in ["TELEGRAM_TOKEN", "SUPABASE_URL", "SUPABASE_KEY", "BOT_ADMIN_ID", "LOG_LEVEL"]:
            value = os.getenv(key)
            logger.error(f"  {key}: {'SET' if value else 'MISSING'}")
        raise ValueError("TELEGRAM_TOKEN must be set in environment variables")
    
    # Create application
    # 🟢 FIX: Increase timeout to 60 seconds to fix Railway crashing
    # 🟢 FIX: Optimized timings for faster response
    # connect_timeout=30: Wait 30s to establish connection (prevents startup crashes)
    # read_timeout=10: If no data for 10s, refresh the connection (fixes the lag!)
# 🟢 FIX: Increase Pool Size to handle spam bursts
    # 🟢 FIX: Increased Pool Size, Removed the invalid parameter
    
    request = HTTPXRequest(connect_timeout=60, read_timeout=60)
    application = Application.builder().token(token).request(request).build()
    
    application = Application.builder().token(token).request(request).build()

    # Import handlers
    from src.handlers.commands import start, help_command, stats
    from src.handlers.moderation import warn, ban, unmute, addword
    from src.handlers.message_handler import handle_text, check_media, handle_approval
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CommandHandler("warn", warn))
    application.add_handler(CommandHandler("ban", ban))
    application.add_handler(CommandHandler("unmute", unmute))
    application.add_handler(CommandHandler("addword", addword))
    # 🟢 NEW: Approval Handler (Listens for "تایید" in Private Chat)
    # 🟢 FIX: Listen for BOTH "تایید" (Approve) and "رد" (Reject)
    application.add_handler(MessageHandler(filters.Regex(r"^(تایید|رد)$") & filters.ChatType.PRIVATE, handle_approval))
   
    # 🟢 NEW: Separate handlers for stability
    # Handler 1: Catches only Photos and Videos
    # 🟢 FIX: Catch Photos, Videos, GIFs (Animation), and Stickers
    application.add_handler(MessageHandler(
        filters.PHOTO | filters.VIDEO | filters.ANIMATION | filters.Sticker.ALL, 
        check_media
    ))
    
    # Handler 2: Catches only Text and Captions
    application.add_handler(MessageHandler((filters.TEXT | filters.CAPTION) & ~filters.COMMAND, handle_text))
    
    logger.info("✅ Handlers setup completed")
    
    # Setup commands
    await setup_commands(application)
    
    return application


def main():
    """Main function - creates and runs the bot (blocking)"""
    logger.info("🤖 بات شروع شد...")
    
    # Create a new event loop for this thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        # Setup the application using the event loop
        application = loop.run_until_complete(setup_application())
        
        # Run polling - this uses the existing event loop
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    finally:
        loop.close()


if __name__ == "__main__":
    try:
        main()  # This is a blocking call
    except KeyboardInterrupt:
        logger.info("❌ Bot stopped by user")
    except Exception as e:
        logger.error(f"❌ خطای غیرمنتظره: {e}")
        import traceback
        traceback.print_exc()
