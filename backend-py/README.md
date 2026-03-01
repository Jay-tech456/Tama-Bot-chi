# MCP Agent Backend API

A FastAPI backend application with Redis, LangChain, Claude Sonnet 4, and Sanity CMS integration for building MCP (Model Context Protocol) applications.

## 🚀 Features

- **FastAPI** - Modern, fast web framework with automatic API documentation
- **Redis** - Data persistence and caching for agents and conversations
- **LangChain** - Framework for building LLM applications
- **Claude Sonnet 4** - Anthropic's latest AI model via Python SDK
- **Sanity CMS** - Headless content management system (optional)
- **MCP Server** - Model Context Protocol implementation

## 📋 Prerequisites

- Python 3.10 or higher
- Redis server (local or Docker)
- Anthropic API key (for chat functionality)
- Sanity CMS credentials (optional, for content features)

## 🛠️ Installation & Setup

### Step 1: Create Virtual Environment

```bash
cd backend-py
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and configure the following:

**Minimum Required Configuration:**
```env
# Redis (required)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=

# Anthropic Claude (required for chat features)
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx
CLAUDE_MODEL=claude-sonnet-4-20250514
```

**Optional Configuration:**
```env
# Sanity CMS (optional - for content management)
SANITY_PROJECT_ID=your_project_id
SANITY_DATASET=production
SANITY_TOKEN=your_sanity_token

# Application Settings
APP_ENV=development
APP_HOST=0.0.0.0
APP_PORT=8000
LOG_LEVEL=INFO
```

### Step 4: Start Redis Server

**Option A: Using Docker (Recommended)**
```bash
docker run -d --name redis -p 6379:6379 redis:latest
```

**Option B: Using Homebrew (macOS)**
```bash
brew install redis
brew services start redis
```

**Option C: Using apt (Ubuntu/Debian)**
```bash
sudo apt-get update
sudo apt-get install redis-server
sudo systemctl start redis
sudo systemctl enable redis
```

**Verify Redis is running:**
```bash
redis-cli ping
# Should return: PONG
```

### Step 5: Run the Application

**Option A: Using Python directly**
```bash
python main.py
```

**Option B: Using uvicorn with auto-reload (Development)**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Option C: Using uvicorn for production**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Step 6: Verify Installation

Open your browser and visit:

- **API Documentation (Swagger)**: http://localhost:8000/docs
- **API Documentation (ReDoc)**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

You should see a health check response like:
```json
{
  "status": "healthy",
  "redis": "connected",
  "timestamp": "2024-01-01T00:00:00.000000+00:00"
}
```

## 📚 API Endpoints

### Health & Info
- `GET /` - Root endpoint with API info
- `GET /health` - Health check with service status

### Agent Management
- `POST /agents` - Create a new agent
- `GET /agents` - List all agents
- `GET /agents/{agent_id}` - Get specific agent
- `PUT /agents/{agent_id}` - Update agent
- `DELETE /agents/{agent_id}` - Delete agent

### Chat & Conversations
- `POST /chat` - Send message to agent and get response
- `GET /agents/{agent_id}/conversation` - Get conversation history
- `DELETE /agents/{agent_id}/conversation` - Clear conversation history

### MCP (Model Context Protocol)
- `GET /mcp/tools` - List available MCP tools
- `GET /mcp/resources` - List available MCP resources
- `POST /mcp/tools/{tool_name}` - Execute an MCP tool
- `GET /mcp/resources/{resource_uri}` - Read an MCP resource

### Sanity CMS Content (Optional)
- `POST /content/search` - Search content in Sanity
- `GET /content/{document_id}` - Get document by ID
- `GET /content/type/{doc_type}` - Get documents by type

## 💡 Usage Examples

### 1. Create an Agent

```bash
curl -X POST http://localhost:8000/agents \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Customer Support Agent",
    "description": "Helpful customer support assistant",
    "system_prompt": "You are a helpful and friendly customer support agent. Always be professional and empathetic.",
    "temperature": 0.7,
    "max_tokens": 4096
  }'
```

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Customer Support Agent",
  "description": "Helpful customer support assistant",
  "system_prompt": "You are a helpful and friendly customer support agent...",
  "temperature": 0.7,
  "max_tokens": 4096,
  "status": "active",
  "created_at": "2024-01-01T00:00:00.000000+00:00",
  "updated_at": "2024-01-01T00:00:00.000000+00:00",
  "metadata": {}
}
```

### 2. Chat with Agent

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "550e8400-e29b-41d4-a716-446655440000",
    "message": "Hello! I need help with my account.",
    "use_sanity_content": false
  }'
```

**Response:**
```json
{
  "agent_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "Hello! I need help with my account.",
  "response": "Hello! I'd be happy to help you with your account. What specific issue are you experiencing?",
  "timestamp": "2024-01-01T00:00:00.000000+00:00",
  "metadata": null
}
```

### 3. Get Conversation History

```bash
curl http://localhost:8000/agents/550e8400-e29b-41d4-a716-446655440000/conversation?limit=10
```

### 4. List All Agents

```bash
curl http://localhost:8000/agents
```

### 5. Search Sanity Content (if configured)

```bash
curl -X POST http://localhost:8000/content/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "product documentation",
    "content_type": "article",
    "limit": 10
  }'
```

## 📁 Project Structure

```
backend-py/
├── main.py                 # FastAPI application entry point
├── config.py              # Configuration and settings management
├── models.py              # Pydantic data models and schemas
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .env                  # Your environment variables (create this)
├── .gitignore            # Git ignore rules
└── services/
    ├── __init__.py       # Services package initialization
    ├── redis_service.py  # Redis operations and caching
    ├── sanity_service.py # Sanity CMS integration
    ├── agent_service.py  # LangChain/Claude integration
    └── mcp_server.py     # MCP server implementation
```

## 🔧 Development

### Running in Development Mode

```bash
# With auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# With custom log level
uvicorn main:app --reload --log-level debug
```

### Code Quality Tools

```bash
# Format code
black .
isort .

# Type checking
mypy .

# Linting
flake8 .
pylint *.py services/*.py
```

### Running Tests

```bash
pytest
pytest --cov=. --cov-report=html
```

## 🐛 Troubleshooting

### Redis Connection Failed

**Problem:** `Redis connection failed - some features may not work`

**Solutions:**
1. Check if Redis is running:
   ```bash
   redis-cli ping
   ```
2. Verify Redis host and port in `.env`:
   ```env
   REDIS_HOST=localhost
   REDIS_PORT=6379
   ```
3. Check if Redis requires authentication:
   ```env
   REDIS_PASSWORD=your_password
   ```
4. Restart Redis:
   ```bash
   # Docker
   docker restart redis
   
   # Homebrew
   brew services restart redis
   
   # Linux
   sudo systemctl restart redis
   ```

### Anthropic API Key Not Working

**Problem:** `Anthropic API key not configured` or chat fails

**Solutions:**
1. Get your API key from https://console.anthropic.com/
2. Add it to `.env`:
   ```env
   ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx
   ```
3. Restart the application
4. Check API usage limits in Anthropic console
5. Verify the model name is correct:
   ```env
   CLAUDE_MODEL=claude-sonnet-4-20250514
   ```

### Import Errors

**Problem:** `ModuleNotFoundError` or import errors

**Solutions:**
1. Ensure virtual environment is activated:
   ```bash
   source venv/bin/activate
   ```
2. Reinstall dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Check Python version (requires 3.10+):
   ```bash
   python --version
   ```

### Port Already in Use

**Problem:** `Address already in use`

**Solutions:**
1. Use a different port:
   ```bash
   uvicorn main:app --port 8001
   ```
2. Or kill the process using port 8000:
   ```bash
   # macOS/Linux
   lsof -ti:8000 | xargs kill -9
   
   # Windows
   netstat -ano | findstr :8000
   taskkill /PID <PID> /F
   ```

### Sanity CMS Errors

**Problem:** Sanity queries failing

**Solutions:**
1. Verify credentials in `.env`:
   ```env
   SANITY_PROJECT_ID=your_project_id
   SANITY_TOKEN=your_token
   ```
2. Check token permissions in Sanity dashboard
3. Verify API version compatibility
4. Test GROQ queries in Sanity Vision

## 🔐 Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `REDIS_HOST` | Yes | `localhost` | Redis server hostname |
| `REDIS_PORT` | Yes | `6379` | Redis server port |
| `REDIS_USERNAME` | No | `default` | Redis username |
| `REDIS_PASSWORD` | No | `""` | Redis password |
| `REDIS_DB` | No | `0` | Redis database number |
| `ANTHROPIC_API_KEY` | Yes* | `""` | Anthropic API key for Claude |
| `CLAUDE_MODEL` | No | `claude-sonnet-4-20250514` | Claude model version |
| `SANITY_PROJECT_ID` | No | `""` | Sanity project ID |
| `SANITY_DATASET` | No | `production` | Sanity dataset name |
| `SANITY_API_VERSION` | No | `2024-01-01` | Sanity API version |
| `SANITY_TOKEN` | No | `""` | Sanity API token |
| `APP_ENV` | No | `development` | Application environment |
| `APP_HOST` | No | `0.0.0.0` | Server host |
| `APP_PORT` | No | `8000` | Server port |
| `LOG_LEVEL` | No | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `CORS_ORIGINS` | No | `["http://localhost:3000","http://localhost:5173"]` | Allowed CORS origins |

*Required for chat functionality

## 🚢 Deployment

### Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:

```bash
docker build -t mcp-backend .
docker run -d -p 8000:8000 --env-file .env mcp-backend
```

### Production Considerations

1. **Use a process manager:**
   ```bash
   gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```

2. **Set up HTTPS** with nginx or Caddy

3. **Configure proper CORS origins** in `.env`

4. **Use environment-specific configs** for production

5. **Set up monitoring** and logging

6. **Use managed Redis** (AWS ElastiCache, Redis Cloud, etc.)

## 📖 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LangChain Documentation](https://python.langchain.com/)
- [Anthropic Claude API](https://docs.anthropic.com/)
- [Redis Documentation](https://redis.io/docs/)
- [Sanity CMS Documentation](https://www.sanity.io/docs)

## 📝 License

MIT