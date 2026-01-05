"""
Entry point for Railway deployment
Starts the Telegram bot
"""

import logging
import os
from dotenv import load_dotenv
from keep_alive import keep_alive

# Load environment variables
load_dotenv(override=False)

# Setup logging before importing bot
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=os.getenv("LOG_LEVEL", "INFO")
)
logger = logging.getLogger(__name__)

logger.info("🚀 Starting bot from main.py...")

try:
    from src.bot import main
    logger.info("✅ Successfully imported main from src.bot")
    
    # 🟢 NEW: Start the fake web server to keep the bot alive on Render
    keep_alive()
    logger.info("✅ Keep-alive server started")

    # Start the bot (This blocks the script, so keep_alive must be above it)
    main()  
except ImportError as e:
    logger.error(f"❌ Import error: {e}", exc_info=True)
    raise
except KeyboardInterrupt:
    logger.info("❌ Bot stopped by user")
except Exception as e:
    logger.error(f"❌ خطای غیرمنتظره: {e}", exc_info=True)
    raise