# MCP Server

The Model Context Protocol (MCP) server for the TamaBotchi AI agent. Provides centralized access to user data, conversation history, and preferences.

## Architecture

The MCP server bridges three data sources:
- **Sanity.io** - User profiles and message templates (CMS)
- **Redis** - Conversation history and general caching (fast, temporary storage)
- **SQLite** - User preferences and interaction logs (local, persistent storage)

## Features

### User Profiles (Sanity.io)
- Store and retrieve user profiles with interests, industry, goals
- Update profile information
- Query profiles for matching

### Conversation History (Redis)
- Cache conversation messages with timestamps
- Retrieve recent conversation history
- Automatic expiration (24-hour TTL by default)
- Supports fast lookups for agent context

### User Preferences (SQLite)
- Store user preferences for conversation style
- Manage permission settings for autonomous actions
- Track high-match thresholds and auto-scheduling preferences
- Persistent local storage

### Message Templates (Sanity.io)
- Retrieve pre-defined message templates
- Templates for introductions, follow-ups, meeting requests
- Customizable template variables

### Interaction Logs (SQLite)
- Log all user interactions (messages, meetings, permissions)
- Track interaction history between users
- Queryable interaction timeline

### General Caching (Redis)
- Key-value caching for arbitrary data
- Configurable TTL
- Fast access for frequently-used data

## API Endpoints

### Health Check
- `GET /health` - Check server and service health

### User Profiles
- `GET /profiles/{user_id}` - Get user profile
- `PATCH /profiles/{user_id}` - Update user profile

### Conversations
- `GET /conversations/{conversation_id}` - Get conversation history
- `POST /conversations/{conversation_id}/messages` - Save message to conversation

### User Preferences
- `GET /preferences/{user_id}` - Get user preferences (returns defaults if not found)
- `PATCH /preferences/{user_id}` - Update user preferences

### Message Templates
- `GET /templates?type={template_type}` - Get message templates by type

### Interaction Logs
- `POST /interactions` - Log an interaction between users

### Caching
- `GET /cache/{key}` - Get cached value
- `POST /cache/{key}` - Set cached value

## Setup

### 1. Install Dependencies

```bash
cd mcp-server
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Edit `.env`:

```bash
# Sanity Configuration
SANITY_PROJECT_ID=c0j8rp13
SANITY_DATASET=production
SANITY_API_TOKEN=your_token_here  # Get from https://www.sanity.io/manage/project/c0j8rp13/api

# Redis Configuration
REDIS_HOST=localhost  # Or use Upstash/Redis Cloud URL
REDIS_PORT=6379
REDIS_PASSWORD=       # Optional for local Redis

# SQLite Configuration
SQLITE_DB_PATH=./data/tama.db  # Automatically created

# Server Configuration
SERVER_PORT=5002
```

### 3. Get Sanity API Token

1. Go to https://www.sanity.io/manage/project/c0j8rp13/api
2. Click "Add API Token"
3. Give it a name (e.g., "MCP Server")
4. Select "Editor" permissions
5. Copy the token to your `.env` file

### 4. Setup Redis

**Option A: Local Redis (requires sudo)**
```bash
sudo apt install redis-server
sudo systemctl start redis
```

**Option B: Cloud Redis (recommended)**

Use [Upstash](https://upstash.com/) free tier:
1. Create account at https://upstash.com/
2. Create a Redis database
3. Copy the connection URL
4. Update `.env` with Upstash credentials:
```bash
REDIS_HOST=your-upstash-url.upstash.io
REDIS_PORT=6379
REDIS_PASSWORD=your-upstash-password
```

### 5. Run the Server

```bash
python main.py
```

Server will start on http://localhost:5002

Visit http://localhost:5002/docs for interactive API documentation.

## Testing

Test the server is working:

```bash
# Health check
curl http://localhost:5002/health

# Get user preferences (will return defaults for new user)
curl http://localhost:5002/preferences/test_user_123

# Save a conversation message
curl -X POST http://localhost:5002/conversations/conv_123/messages \
  -H "Content-Type: application/json" \
  -d '{
    "sender": "user_123",
    "message": "Hello!",
    "metadata": {"event": "Test Event"}
  }'

# Get conversation history
curl http://localhost:5002/conversations/conv_123
```

## Data Models

### User Profile (Sanity)
```typescript
{
  userId: string
  name: string
  email: string
  phone?: string
  interests: string[]
  industry: string
  role: string
  seniority: string
  goals: string[]
  bio?: string
  location?: string
  linkedinUrl?: string
  twitterHandle?: string
  availability?: object
}
```

### User Preferences (SQLite)
```typescript
{
  user_id: string
  conversation_style: {
    tone: string          // professional, casual, friendly
    length: string        // brief, moderate, detailed
    formality: string     // formal, semi-formal, casual
    emoji_usage: boolean
  }
  permissions: {
    send_message: string        // always_ask, auto_high_match, always_auto, never
    schedule_meeting: string
    send_email: string
    share_profile: string
    request_connection: string
  }
  high_match_threshold: number  // 0.0 - 1.0
  auto_schedule_enabled: boolean
}
```

### Conversation Message (Redis)
```typescript
{
  sender: string
  message: string
  timestamp: string  // ISO 8601
  metadata: object
}
```

### Message Template (Sanity)
```typescript
{
  templateType: string  // introduction, follow_up, meeting_request
  name: string
  content: string
  variables: string[]
  context: object
}
```

## Integration with Agent

The agent uses the MCP client (`agent/tools/mcp_client.py`) to communicate with this server:

```python
from tools.mcp_client import MCPClient

mcp = MCPClient()

# Get user profile
profile = mcp.get_user_profile("user_123")

# Get conversation history
messages = mcp.get_conversation_history("conv_123")

# Save message
mcp.save_conversation_message("conv_123", "agent", "Hello!")

# Get preferences
prefs = mcp.get_user_preferences("user_123")
```

## Caching Strategy

**What goes in Redis (temporary, fast):**
- Conversation history (24-hour TTL)
- Frequently accessed data
- Session data
- Match scores

**What goes in SQLite (permanent, local):**
- User preferences
- Interaction logs
- System configuration

**What goes in Sanity (permanent, cloud):**
- User profiles
- Message templates
- Content that needs CMS features

## Troubleshooting

**Redis connection failed:**
- Check if Redis is running: `redis-cli ping`
- Or use cloud Redis (Upstash)
- Server will still work with degraded caching features

**Sanity write operations fail:**
- Ensure `SANITY_API_TOKEN` is set in `.env`
- Verify token has Editor permissions
- Read operations work without token

**SQLite errors:**
- Ensure `data/` directory exists
- Check file permissions
- Database is created automatically on first run

## Development

Run with auto-reload:
```bash
uvicorn main:app --reload --port 5002
```

View logs:
```bash
python main.py  # Logs to stdout
```

## Production Considerations

- Add authentication/authorization
- Use connection pooling for Redis
- Add rate limiting
- Monitor cache hit rates
- Set up proper logging
- Use environment-specific configs
- Add health check monitoring
- Consider Redis Sentinel for HA
