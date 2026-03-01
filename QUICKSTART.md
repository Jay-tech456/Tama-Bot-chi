# TamaBotchi Quick Start Guide

Get TamaBotchi up and running in 5 minutes!

## Prerequisites Check

- [ ] Python 3.9+ installed (`python --version`)
- [ ] macOS computer available (for iMessage integration)
- [ ] Anthropic API key ([get one here](https://console.anthropic.com/))

## Step 1: Clone and Setup (2 min)

```bash
cd Tama-Bot-Chi

# Setup Agent
cd agent
pip install -r requirements.txt
cp .env.example .env
```

Edit `agent/.env` and add your Anthropic API key:
```bash
ANTHROPIC_API_KEY=sk-ant-xxxxx
```

## Step 2: Setup iMessage Server (Mac only, 3 min)

```bash
cd ../imessage-server
pip install -r requirements.txt
```

**Grant Full Disk Access:**
1. Open System Preferences → Security & Privacy → Privacy
2. Click "Full Disk Access" in left sidebar
3. Click the lock icon to make changes
4. Click "+" and add Terminal (or iTerm if you use that)
5. Restart your Terminal app

## Step 3: Start the Services

**Terminal 1 - iMessage Server (Mac):**
```bash
cd imessage-server
python server.py
```

You should see:
```
TamaBotchi iMessage Bridge Server starting...
📱 Make sure you have granted Full Disk Access to Terminal/iTerm
```

**Terminal 2 - Agent API:**
```bash
cd agent
python main.py
```

You should see:
```
Starting TamaBotchi Agent API...
Agent: TamaBotchi
```

## Step 4: Test It!

Open a third terminal and test the system:

```bash
# Check health
curl http://localhost:5000/health

# Test detection (simulates finding someone nearby)
curl -X POST http://localhost:5000/users/test_user/detected \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user",
    "other_user_id": "other_user",
    "context": {
      "event_name": "Test Event",
      "location": "San Francisco"
    }
  }'
```

## Step 5: Explore the API

Visit the interactive API docs:
- Agent API: http://localhost:5000/docs
- iMessage Server: http://localhost:5001/docs

## What's Next?

1. **Your team builds:** MCP server (port 5002) for Sanity.io/Redis/SQLite
2. **Create test user profiles** in the MCP server
3. **Setup Gmail API** for calendar/email integration (see main README)
4. **Build mobile app** for proximity detection

## Troubleshooting

**iMessage server won't start:**
- Make sure you granted Full Disk Access
- Restart Terminal after granting access
- Open Messages app and sign in first

**Agent API errors:**
- Check your Anthropic API key in `.env`
- Make sure all dependencies installed: `pip install -r requirements.txt`

**Can't connect to MCP server:**
- That's expected! Your team needs to build it first
- The agent will show warnings but still work for testing

## Testing Without MCP Server

For testing before the MCP server is ready, you can mock the responses. The agent will gracefully handle missing MCP data.

## Need Help?

Check the main [README.md](README.md) for full documentation and architecture details.

---

🎉 **You're ready to start building!**
