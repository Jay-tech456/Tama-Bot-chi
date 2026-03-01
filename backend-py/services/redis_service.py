import redis
import json
from typing import Optional, List, Dict, Any
from datetime import datetime
from config import settings


class RedisService:
    """Redis service for data persistence and caching"""
    
    def __init__(self):
        self.client = redis.Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            username=settings.redis_username,
            password=settings.redis_password,
            db=settings.redis_db,
            decode_responses=True
        )
    
    def ping(self) -> bool:
        """Check Redis connection"""
        try:
            return self.client.ping()
        except Exception as e:
            print(f"Redis connection error: {e}")
            return False
    
    # Agent operations
    def save_agent(self, agent_id: str, agent_data: Dict[str, Any]) -> bool:
        """Save agent data to Redis"""
        try:
            key = f"agent:{agent_id}"
            self.client.hset(key, mapping=self._serialize_dict(agent_data))
            self.client.sadd("agents:all", agent_id)
            return True
        except Exception as e:
            print(f"Error saving agent: {e}")
            return False
    
    def get_agent(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve agent data from Redis"""
        try:
            key = f"agent:{agent_id}"
            data = self.client.hgetall(key)
            return self._deserialize_dict(data) if data else None
        except Exception as e:
            print(f"Error retrieving agent: {e}")
            return None
    
    def get_all_agents(self) -> List[Dict[str, Any]]:
        """Retrieve all agents"""
        try:
            agent_ids = self.client.smembers("agents:all")
            agents = []
            for agent_id in agent_ids:
                agent = self.get_agent(agent_id)
                if agent:
                    agents.append(agent)
            return agents
        except Exception as e:
            print(f"Error retrieving agents: {e}")
            return []
    
    def update_agent(self, agent_id: str, updates: Dict[str, Any]) -> bool:
        """Update agent data"""
        try:
            key = f"agent:{agent_id}"
            if not self.client.exists(key):
                return False
            self.client.hset(key, mapping=self._serialize_dict(updates))
            return True
        except Exception as e:
            print(f"Error updating agent: {e}")
            return False
    
    def delete_agent(self, agent_id: str) -> bool:
        """Delete agent from Redis"""
        try:
            key = f"agent:{agent_id}"
            self.client.delete(key)
            self.client.srem("agents:all", agent_id)
            # Delete associated conversation history
            self.client.delete(f"conversation:{agent_id}")
            return True
        except Exception as e:
            print(f"Error deleting agent: {e}")
            return False
    
    # Conversation operations
    def save_message(self, agent_id: str, role: str, content: str, metadata: Optional[Dict] = None) -> bool:
        """Save a message to conversation history"""
        try:
            key = f"conversation:{agent_id}"
            message = {
                "role": role,
                "content": content,
                "timestamp": datetime.utcnow().isoformat(),
                "metadata": metadata or {}
            }
            self.client.rpush(key, json.dumps(message))
            return True
        except Exception as e:
            print(f"Error saving message: {e}")
            return False
    
    def get_conversation_history(self, agent_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Retrieve conversation history"""
        try:
            key = f"conversation:{agent_id}"
            messages = self.client.lrange(key, -limit, -1)
            return [json.loads(msg) for msg in messages]
        except Exception as e:
            print(f"Error retrieving conversation: {e}")
            return []
    
    def clear_conversation(self, agent_id: str) -> bool:
        """Clear conversation history"""
        try:
            key = f"conversation:{agent_id}"
            self.client.delete(key)
            return True
        except Exception as e:
            print(f"Error clearing conversation: {e}")
            return False
    
    # Cache operations
    def cache_set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """Set a cache value with TTL"""
        try:
            self.client.setex(key, ttl, json.dumps(value))
            return True
        except Exception as e:
            print(f"Error setting cache: {e}")
            return False
    
    def cache_get(self, key: str) -> Optional[Any]:
        """Get a cache value"""
        try:
            value = self.client.get(key)
            return json.loads(value) if value else None
        except Exception as e:
            print(f"Error getting cache: {e}")
            return None
    
    # Helper methods
    def _serialize_dict(self, data: Dict[str, Any]) -> Dict[str, str]:
        """Serialize dictionary values for Redis storage"""
        return {k: json.dumps(v) if not isinstance(v, str) else v for k, v in data.items()}
    
    def _deserialize_dict(self, data: Dict[str, str]) -> Dict[str, Any]:
        """Deserialize dictionary values from Redis"""
        result = {}
        for k, v in data.items():
            try:
                result[k] = json.loads(v)
            except (json.JSONDecodeError, TypeError):
                result[k] = v
        return result


# Singleton instance
redis_service = RedisService()
