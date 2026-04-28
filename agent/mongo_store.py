"""
MongoDB Atlas persistent memory store for TamaBotchi.

Stores every iMessage exchange so the agent can recall prior conversations
with each sender across sessions (beyond Redis's 24-hour TTL).

Collections:
  messages         - one document per message (incoming or outgoing)
  contact_profiles - one document per unique sender with relationship context
"""
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.errors import ConnectionFailure, OperationFailure, PyMongoError

logger = logging.getLogger(__name__)

# Database and collection names
_DB_NAME = "tamabotchi"
_MESSAGES_COLLECTION = "messages"
_PROFILES_COLLECTION = "contact_profiles"


class MongoStore:
    """
    MongoDB Atlas client for TamaBotchi persistent conversation memory.

    Provides two operations:
      - save_message: persist an individual message (incoming or agent reply)
      - get_recent_history: fetch the last N messages for a given sender
      - upsert_contact_profile: update relationship metadata for a sender
      - get_contact_profile: retrieve relationship metadata for a sender

    All methods degrade gracefully: on any Atlas error they log a warning
    and return a safe empty value rather than raising, so the agent keeps
    working even when Atlas is temporarily unavailable.
    """

    def __init__(self, uri: str) -> None:
        """
        Connect to MongoDB Atlas.

        Args:
            uri: MongoDB connection string (mongodb+srv://...)

        Raises:
            ConnectionFailure: If the initial ping to Atlas fails
            ValueError: If uri is empty or None
        """
        if not uri:
            raise ValueError("MongoDB URI must be a non-empty connection string")

        self._client: MongoClient = MongoClient(
            uri,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=5000,
            socketTimeoutMS=10000,
        )

        # Verify connectivity immediately so callers can catch at init time
        self._client.admin.command("ping")

        self._db: Database = self._client[_DB_NAME]
        self._messages: Collection = self._db[_MESSAGES_COLLECTION]
        self._profiles: Collection = self._db[_PROFILES_COLLECTION]

        self._ensure_indexes()
        logger.info("MongoStore connected to Atlas (db=%s)", _DB_NAME)

    def _ensure_indexes(self) -> None:
        """
        Create indexes once on first connection.

        Index strategy:
          messages: (sender_id, timestamp DESC) for history lookups per sender
          contact_profiles: (sender_id ASC, unique) for O(1) profile upserts
        """
        try:
            self._messages.create_index(
                [("sender_id", ASCENDING), ("timestamp", DESCENDING)],
                name="sender_timestamp",
                background=True,
            )
            self._profiles.create_index(
                [("sender_id", ASCENDING)],
                name="sender_unique",
                unique=True,
                background=True,
            )
        except PyMongoError as exc:
            logger.warning("Could not create Atlas indexes: %s", exc)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def save_message(
        self,
        conversation_id: str,
        sender_id: str,
        text: str,
        is_from_agent: bool,
    ) -> bool:
        """
        Persist a single message to the messages collection.

        Args:
            conversation_id: Unique thread identifier (e.g. imsg_user_phone)
            sender_id: Phone number or email of the human participant
            text: Message body
            is_from_agent: True when TamaBotchi sent this message

        Returns:
            True on success, False if the write failed (non-fatal)
        """
        doc: Dict[str, Any] = {
            "conversation_id": conversation_id,
            "sender_id": sender_id,
            "text": text,
            "is_from_agent": is_from_agent,
            "timestamp": datetime.now(tz=timezone.utc),
        }
        try:
            self._messages.insert_one(doc)
            return True
        except PyMongoError as exc:
            logger.warning("Atlas write failed for conversation %s: %s", conversation_id, exc)
            return False

    def get_recent_history(
        self,
        sender_id: str,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        Fetch the most recent messages for a sender, ordered oldest-first.

        Retrieves messages in both directions (incoming from sender AND agent
        replies to that sender) so Claude sees the full back-and-forth.

        Args:
            sender_id: Phone number or email identifying the contact
            limit: Maximum number of messages to return (default 10)

        Returns:
            List of message dicts with keys: sender_id, text, is_from_agent,
            timestamp. Empty list if none found or on Atlas error.
        """
        try:
            cursor = (
                self._messages.find(
                    {"sender_id": sender_id},
                    {"_id": 0, "sender_id": 1, "text": 1, "is_from_agent": 1, "timestamp": 1},
                )
                .sort("timestamp", DESCENDING)
                .limit(limit)
            )
            # Reverse so the list is chronological (oldest first)
            messages: List[Dict[str, Any]] = list(cursor)
            messages.reverse()
            return messages
        except PyMongoError as exc:
            logger.warning("Atlas history fetch failed for sender %s: %s", sender_id, exc)
            return []

    def upsert_contact_profile(
        self,
        sender_id: str,
        updates: Dict[str, Any],
    ) -> bool:
        """
        Create or update the relationship profile for a contact.

        Args:
            sender_id: Phone number or email identifying the contact
            updates: Fields to set or merge into the profile document.
                     Common keys: relationship_notes (str), topics (list[str])

        Returns:
            True on success, False if the write failed (non-fatal)
        """
        try:
            self._profiles.update_one(
                {"sender_id": sender_id},
                {
                    "$set": {**updates, "last_seen": datetime.now(tz=timezone.utc)},
                    "$inc": {"message_count": 0},  # ensure field exists
                    "$setOnInsert": {"sender_id": sender_id, "message_count": 0},
                },
                upsert=True,
            )
            return True
        except PyMongoError as exc:
            logger.warning("Atlas profile upsert failed for sender %s: %s", sender_id, exc)
            return False

    def increment_message_count(self, sender_id: str) -> bool:
        """
        Increment the total message count for a contact.

        Args:
            sender_id: Phone number or email identifying the contact

        Returns:
            True on success, False on failure (non-fatal)
        """
        try:
            self._profiles.update_one(
                {"sender_id": sender_id},
                {
                    "$inc": {"message_count": 1},
                    "$set": {"last_seen": datetime.now(tz=timezone.utc)},
                    "$setOnInsert": {"sender_id": sender_id},
                },
                upsert=True,
            )
            return True
        except PyMongoError as exc:
            logger.warning("Atlas count increment failed for sender %s: %s", sender_id, exc)
            return False

    def get_contact_profile(
        self,
        sender_id: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieve relationship metadata for a contact.

        Args:
            sender_id: Phone number or email identifying the contact

        Returns:
            Profile dict if found, None if the contact is unknown or on error.
            Keys: sender_id, last_seen, message_count, topics, relationship_notes
        """
        try:
            doc = self._profiles.find_one(
                {"sender_id": sender_id},
                {"_id": 0},
            )
            return doc  # type: ignore[return-value]
        except PyMongoError as exc:
            logger.warning("Atlas profile fetch failed for sender %s: %s", sender_id, exc)
            return None

    def close(self) -> None:
        """Close the underlying MongoDB connection cleanly."""
        try:
            self._client.close()
        except PyMongoError as exc:
            logger.warning("Error closing MongoDB connection: %s", exc)
