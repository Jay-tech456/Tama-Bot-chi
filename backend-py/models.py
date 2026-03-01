from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
from enum import Enum


class AgentStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PROCESSING = "processing"


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class Message(BaseModel):
    role: MessageRole
    content: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Optional[Dict[str, Any]] = None


class AgentCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    system_prompt: Optional[str] = None
    temperature: float = Field(default=0.7, ge=0.0, le=1.0)
    max_tokens: int = Field(default=4096, ge=1, le=200000)
    metadata: Optional[Dict[str, Any]] = None


class AgentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    system_prompt: Optional[str] = None
    temperature: Optional[float] = Field(None, ge=0.0, le=1.0)
    max_tokens: Optional[int] = Field(None, ge=1, le=200000)
    status: Optional[AgentStatus] = None
    metadata: Optional[Dict[str, Any]] = None


class Agent(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    system_prompt: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 4096
    status: AgentStatus = AgentStatus.ACTIVE
    created_at: datetime
    updated_at: datetime
    metadata: Optional[Dict[str, Any]] = None


class ChatRequest(BaseModel):
    agent_id: str
    message: str
    context: Optional[Dict[str, Any]] = None
    use_sanity_content: bool = False


class ChatResponse(BaseModel):
    agent_id: str
    message: str
    response: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Optional[Dict[str, Any]] = None


class ContentQuery(BaseModel):
    query: str
    content_type: Optional[str] = None
    filters: Optional[Dict[str, Any]] = None
    limit: int = Field(default=10, ge=1, le=100)
