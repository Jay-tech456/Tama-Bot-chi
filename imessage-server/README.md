# TamaBotchi iMessage Bridge Server

This server runs on macOS and provides a REST API for sending and receiving iMessages.

## Setup Instructions (for Mac user)

### 1. Prerequisites
- macOS with Messages app configured and signed in to iMessage
- Python 3.8 or higher
- Terminal with Full Disk Access

### 2. Grant Full Disk Access

1. Open **System Preferences** → **Security & Privacy** → **Privacy** tab
2. Select **Full Disk Access** from the left sidebar
3. Click the lock icon and authenticate
4. Click the **+** button and add your Terminal app (or iTerm if you use that)
5. Restart your Terminal

### 3. Install Dependencies

```bash
cd imessage-server
pip install -r requirements.txt
```

### 4. Run the Server

```bash
python server.py
```

Or with uvicorn directly:
```bash
uvicorn server:app --host 0.0.0.0 --port 5001 --reload
```

The server will start on `http://0.0.0.0:5001`

Visit `http://localhost:5001/docs` for interactive API documentation.

## API Endpoints

### Health Check
```bash
GET /health
```

### Send iMessage
```bash
POST /send
Content-Type: application/json

{
  "recipient": "+1234567890",
  "message": "Hello from TamaBotchi!"
}
```

### Get Recent Messages
```bash
GET /messages?limit=50
```

### Get Send Logs
```bash
GET /logs?limit=100
```

## Testing

Send a test message:
```bash
curl -X POST http://localhost:5001/send \
  -H "Content-Type: application/json" \
  -d '{"recipient": "+1234567890", "message": "Test from TamaBotchi!"}'
```

## Security Notes

- This server should only be accessible within your trusted network
- Consider adding authentication tokens in production
- Keep the Mac awake and connected to prevent service interruption
- Messages database access requires Full Disk Access permission

## Troubleshooting

**Error: "Messages database not found"**
- Ensure Full Disk Access is granted to Terminal
- Restart Terminal after granting access

**Error: "AppleScript execution failed"**
- Open Messages app and ensure you're signed in
- Send a manual test message first
- Check that iMessage is enabled in Messages preferences

**Messages not sending**
- Verify the recipient format (phone number or email)
- Check Messages app preferences
- Review logs at `/logs` endpoint
