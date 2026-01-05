"""
Supabase Database Module
Handles all database operations for the Telegram bot
"""

import os
import logging
from typing import List, Optional
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()
logger = logging.getLogger(__name__)


class DatabaseManager:
    """Database manager for Supabase operations"""
    
    def __init__(self):
        """Initialize Supabase client and cache"""
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        
        if not self.url or not self.key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in .env file")
        
        self.client: Client = create_client(self.url, self.key)
        self.initialize_default_banned_words() 
        self.banned_words_cache: List[str] = []
        self._cache_loaded = False
        
        logger.info("DatabaseManager initialized")
    
    # ==================== User Management ====================
    
    def initialize_user(self, user_id: int, username: str) -> Optional[dict]:
        """
        Add a user to the users table if they don't exist.
        
        Args:
            user_id: Telegram user ID
            username: Telegram username
            
        Returns:
            User data or None if error
        """
        try:
            # Check if user exists
            response = self.client.table("users").select("user_id").eq("user_id", user_id).execute()
            
            if response.data:
                logger.info(f"User {user_id} already exists")
                return response.data[0]
            
            # Create new user
            new_user = {
                "user_id": user_id,
                "username": username,
                "warn_count": 0
            }
            response = self.client.table("users").insert(new_user).execute()
            logger.info(f"User {user_id} initialized successfully")
            return response.data[0] if response.data else None
            
        except Exception as e:
            logger.error(f"Error initializing user {user_id}: {e}")
            return None
    
    def add_warn(self, user_id: int) -> Optional[int]:
        """
        Increment the warn count for a user.
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            Updated warn count or None if error
        """
        try:
            # First, ensure user exists
            user = self.client.table("users").select("warn_count").eq("user_id", user_id).execute()
            
            if not user.data:
                logger.warning(f"User {user_id} not found, initializing with 1 warn")
                self.initialize_user(user_id, "unknown")
            
            # Increment warn count
            current_warns = user.data[0]["warn_count"] if user.data else 0
            new_warn_count = current_warns + 1
            
            response = self.client.table("users").update(
                {"warn_count": new_warn_count}
            ).eq("user_id", user_id).execute()
            
            logger.info(f"User {user_id} warned. New warn count: {new_warn_count}")
            return new_warn_count
            
        except Exception as e:
            logger.error(f"Error adding warn to user {user_id}: {e}")
            return None
    
    def get_user_stats(self, user_id: int) -> Optional[dict]:
        """
        Get user statistics including warn count.
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            User stats dictionary or None if error
        """
        try:
            response = self.client.table("users").select("*").eq("user_id", user_id).execute()
            
            if not response.data:
                logger.warning(f"User {user_id} not found")
                return None
            
            user_data = response.data[0]
            return {
                "user_id": user_data["user_id"],
                "username": user_data["username"],
                "warn_count": user_data["warn_count"]
            }
            
        except Exception as e:
            logger.error(f"Error getting stats for user {user_id}: {e}")
            return None

    def get_user_id_by_username(self, username: str) -> Optional[int]:
        """
        Find user ID by username.
        """
        try:
            # Remove @ if present
            clean_username = username.lstrip("@")
            
            # Search in database
            response = self.client.table("users").select("user_id").eq("username", clean_username).execute()
            
            if response.data and len(response.data) > 0:
                return response.data[0]['user_id']
            
            return None
        except Exception as e:
            logger.error(f"Error finding user by username: {e}")
            return None
    
    # ==================== Banned Words Management ====================
    
    def load_banned_words_cache(self) -> bool:
        """
        Load banned words from database into cache.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            response = self.client.table("banned_words").select("word").execute()
            
            self.banned_words_cache = [item["word"].lower() for item in response.data]
            self._cache_loaded = True
            
            logger.info(f"Loaded {len(self.banned_words_cache)} banned words into cache")
            return True
            
        except Exception as e:
            logger.error(f"Error loading banned words cache: {e}")
            self.banned_words_cache = []
            return False
    
    def get_banned_words(self) -> List[str]:
        """
        Get cached list of banned words. Loads from database if cache is empty.
        
        Returns:
            List of banned words
        """
        if not self._cache_loaded or not self.banned_words_cache:
            self.load_banned_words_cache()
        
        return self.banned_words_cache
    
    def initialize_default_banned_words(self) -> bool:
        """
        Initialize database with default Persian banned words if empty.
        
        Returns:
            True if successful
        """
        try:
            # Check if banned words table has any entries
            response = self.client.table("banned_words").select("id").limit(1).execute()
            
            if response.data:
                logger.info("Banned words already exist in database")
                return True
            
            # Default Persian spam and profanity words
            default_words = [
                # Spam/Advertising words
                "تبلیغ",
                "صیغه",
                "لینک",
                "فروش",
                "خرید",
                "کسب درآمد",
                "کار در خانه",
                "کریپتو",
                "بیت کوین",
                # Profanity and explicit words
                "کون",
                "کونی",
                "کونکش",
                "کون گشاد",
                "کص",
                "کصکش",
                "کص کش",
                "کیر",
                "دودول",
                "خایه",
                "گوه",
                "عن",
                "کون کش",
                "کس کش",
                "کسکش",
                "بیشرف",
                "قهبه",
                "جنده",
                "ناموس",
                "بیناموس",
                "بی ناموس",
                "گاییدم",
                "گایید",
                "کیرم",
                "کیرت",
                "گاییدن",
                "گایش",
                "مادرتو",
                "ننتو",
                "مامانتو",
                "حرومزاده",
                "حرامزاده",
                "حروم زاده",
                "حرام زاده",
                "بیخایه",
                "بی خایه"
            ]
            
            # Insert default words
            for word in default_words:
                self.client.table("banned_words").insert({
                    "word": word.lower()
                }).execute()
            
            # Reload cache
            self.load_banned_words_cache()
            logger.info(f"Initialized {len(default_words)} default banned words")
            return True
            
        except Exception as e:
            logger.error(f"Error initializing default banned words: {e}")
            return False
    
    def add_banned_word(self, word: str) -> Optional[dict]:
        """
        Add a word to the banned words list.
        
        Args:
            word: Word to ban
            
        Returns:
            Added word data or None if error
        """
        try:
            word_lower = word.lower()
            
            # Check if word already exists
            response = self.client.table("banned_words").select("word").eq("word", word_lower).execute()
            
            if response.data:
                logger.info(f"Word '{word}' already in banned list")
                return response.data[0]
            
            # Add new banned word
            new_word = {"word": word_lower}
            response = self.client.table("banned_words").insert(new_word).execute()
            
            # Update cache
            if response.data:
                self.banned_words_cache.append(word_lower)
                logger.info(f"Added '{word}' to banned words")
            
            return response.data[0] if response.data else None
            
        except Exception as e:
            logger.error(f"Error adding banned word '{word}': {e}")
            return None
    
    def remove_banned_word(self, word: str) -> bool:
        """
        Remove a word from the banned words list.
        
        Args:
            word: Word to remove
            
        Returns:
            True if successful, False otherwise
        """
        try:
            word_lower = word.lower()
            
            self.client.table("banned_words").delete().eq("word", word_lower).execute()
            
            # Update cache
            if word_lower in self.banned_words_cache:
                self.banned_words_cache.remove(word_lower)
            
            logger.info(f"Removed '{word}' from banned words")
            return True
            
        except Exception as e:
            logger.error(f"Error removing banned word '{word}': {e}")
            return False

    def reset_warns(self, user_id: int) -> bool:
        """Reset user warnings to 0"""
        try:
            self.client.table("users").update({"warn_count": 0}).eq("user_id", user_id).execute()
            logger.info(f"Reset warnings for user {user_id}")
            return True
        except Exception as e:
            logger.error(f"Error resetting warns: {e}")
            return False

# Initialize database manager instance
db = DatabaseManager()
