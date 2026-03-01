"""
Redis cache manager for conversation history and general caching.
"""
import redis
import json
import logging
from typing import Optional, Any, List, Dict
from datetime import datetime

from config import Config

logger = logging.getLogger(__name__)


class RedisCache:
    """Redis cache manager for conversations and general caching."""

    def __init__(self):
        """Initialize Redis connection."""
        self.client = redis.Redis(
            host=Config.REDIS_HOST,
            port=Config.REDIS_PORT,
            db=Config.REDIS_DB,
            password=Config.REDIS_PASSWORD,
            username=Config.REDIS_USERNAME,
            decode_responses=True,
            socket_connect_timeout=5
        )
        self._test_connection()

    def _test_connection(self) -> None:
        """Test Redis connection and log status."""
        try:
            self.client.ping()
            logger.info(f"Connected to Redis at {Config.REDIS_HOST}:{Config.REDIS_PORT}")
        except redis.ConnectionError as e:
            logger.error(f"Failed to connect to Redis: {e}")
            logger.warning("Redis operations will fail until connection is established")

    def is_connected(self) -> bool:
        """
        Check if Redis is connected.

        Returns:
            True if connected, False otherwise
        """
        try:
            return self.client.ping()
        except (redis.ConnectionError, redis.TimeoutError):
            return False

    def get_conversation_history(
        self,
        conversation_id: str,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Get conversation history from cache.

        Args:
            conversation_id: Conversation ID
            limit: Maximum number of messages to retrieve

        Returns:
            List of message dictionaries (newest first)

        Raises:
            redis.ConnectionError: If Redis is not connected
        """
        key = f"conversation:{conversation_id}"

        try:
            # Get messages from sorted set (newest first)
            messages = self.client.zrevrange(key, 0, limit - 1)

            return [json.loads(msg) for msg in messages]

        except redis.ConnectionError as e:
            logger.error(f"Redis connection error getting conversation {conversation_id}: {e}")
            raise

    def save_conversation_message(
        self,
        conversation_id: str,
        sender: str,
        message: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Save a message to conversation history.

        Args:
            conversation_id: Conversation ID
            sender: Message sender ID
            message: Message content
            metadata: Optional message metadata

        Returns:
            True if message saved successfully

        Raises:
            redis.ConnectionError: If Redis is not connected
        """
        key = f"conversation:{conversation_id}"
        timestamp = datetime.utcnow().isoformat()

        message_data = {
            'sender': sender,
            'message': message,
            'timestamp': timestamp,
            'metadata': metadata or {}
        }

        try:
            # Use timestamp as score for sorting
            score = datetime.utcnow().timestamp()
            self.client.zadd(key, {json.dumps(message_data): score})

            # Set TTL on conversation
            self.client.expire(key, Config.CONVERSATION_CACHE_TTL)

            logger.info(f"Saved message to conversation {conversation_id}")
            return True

        except redis.ConnectionError as e:
            logger.error(f"Redis connection error saving message to {conversation_id}: {e}")
            raise

    def get_cached(self, key: str) -> Optional[Any]:
        """
        Get value from cache.

        Args:
            key: Cache key

        Returns:
            Cached value (deserialized from JSON) or None if not found

        Raises:
            redis.ConnectionError: If Redis is not connected
        """
        try:
            value = self.client.get(key)
            if value:
                return json.loads(value)
            return None

        except redis.ConnectionError as e:
            logger.error(f"Redis connection error getting key {key}: {e}")
            raise

    def set_cached(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None
    ) -> bool:
        """
        Set value in cache.

        Args:
            key: Cache key
            value: Value to cache (must be JSON-serializable)
            ttl: Optional time-to-live in seconds

        Returns:
            True if value cached successfully

        Raises:
            redis.ConnectionError: If Redis is not connected
        """
        try:
            serialized = json.dumps(value)
            if ttl:
                self.client.setex(key, ttl, serialized)
            else:
                self.client.set(key, serialized)

            logger.debug(f"Cached key {key} with TTL {ttl}")
            return True

        except redis.ConnectionError as e:
            logger.error(f"Redis connection error setting key {key}: {e}")
            raise

    def delete_cached(self, key: str) -> bool:
        """
        Delete value from cache.

        Args:
            key: Cache key

        Returns:
            True if key was deleted, False if key didn't exist

        Raises:
            redis.ConnectionError: If Redis is not connected
        """
        try:
            result = self.client.delete(key)
            return bool(result)

        except redis.ConnectionError as e:
            logger.error(f"Redis connection error deleting key {key}: {e}")
            raise

    def clear_conversation(self, conversation_id: str) -> bool:
        """
        Clear all messages from a conversation.

        Args:
            conversation_id: Conversation ID

        Returns:
            True if conversation was cleared

        Raises:
            redis.ConnectionError: If Redis is not connected
        """
        key = f"conversation:{conversation_id}"
        return self.delete_cached(key)


# Global cache instance
cache = RedisCache()
