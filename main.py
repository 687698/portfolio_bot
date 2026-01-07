"""
Entry point for Portfolio Bot
Starts the Telegram bot
"""

import logging
import os
import asyncio
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=os.getenv("LOG_LEVEL", "INFO")
)
logger = logging.getLogger(__name__)

logger.info("🚀 Starting bot from main.py...")

try:
    from src.bot import main
    logger.info("✅ Successfully imported main from src.bot")
    
    # We do NOT need keep_alive on PythonAnywhere (it uses Consoles, not Web Services)
    # keep_alive() 

    if __name__ == "__main__":
        main()
        
except ImportError as e:
    logger.error(f"❌ Import error: {e}", exc_info=True)
    raise
except KeyboardInterrupt:
    logger.info("❌ Bot stopped by user")
except Exception as e:
    logger.error(f"❌ Unexpected error: {e}", exc_info=True)
    raise