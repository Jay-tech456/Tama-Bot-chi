# 🐰 TamaBotchi Desktop Pet

A fluffy bunny desktop companion that lives on your macOS desktop and provides comprehensive conversation summaries from the TamaBotchi iMessage AI Agent.

## What It Does

When your device is on **Do Not Disturb**, the TamaBotchi agent handles your iMessage conversations autonomously. The desktop pet bunny:

- **Lives on your desktop** as an always-on-top transparent overlay
- **Shows notification badges** when new conversations arrive
- **Wiggles excitedly** when you have unread messages
- **Click the bunny** → opens a summary panel showing:
  - **Who contacted you** (sender info)
  - **What they want** (intent)
  - **Requirements** (specific asks)
  - **Urgency level** (high/medium/low)
  - **Action items** (what you need to do)
  - **AI-generated one-liner** summary

## Architecture

```
desktop-pet/
├── electron/           # Electron main process (transparent window)
│   ├── main.ts         # Window management, IPC handlers
│   └── preload.ts      # Secure bridge to renderer
├── src/
│   ├── components/     # React functional components
│   │   ├── BunnyPet.tsx           # SVG bunny with animations
│   │   ├── SummaryPanel.tsx       # Conversation list + summaries
│   │   ├── ConversationCard.tsx   # Individual conversation view
│   │   └── NotificationBadge.tsx  # Unread count badge
│   ├── middleware/      # Backend API calls (axios)
│   │   └── api.js       # All agent API endpoints
│   ├── styles/          # Separated CSS files
│   │   ├── App.css
│   │   ├── BunnyPet.css
│   │   ├── SummaryPanel.css
│   │   └── NotificationBadge.css
│   └── artifacts/       # Image assets directory
├── Dockerfile
├── docker-compose.yml
└── package.json
```

## Prerequisites

- **Node.js** >= 18
- **TamaBotchi Agent API** running on `http://127.0.0.1:5000`
- **iMessage Server** running on `http://127.0.0.1:5001`
- **iMessage Watcher** running

## Quick Start

```bash
# Install dependencies
cd desktop-pet
npm install

# Run the desktop pet (Electron + Vite dev server)
npm start
# or
npm run electron:dev

# Run just the React dev server (browser preview)
npm run dev
```

## API Endpoints Used

The pet communicates with these agent API endpoints:

| Endpoint | Method | Description |
|---|---|---|
| `/pet/conversations` | GET | All tracked conversations |
| `/pet/conversations/unread` | GET | Unread conversations only |
| `/pet/conversations/unread/count` | GET | Quick unread count for badge |
| `/pet/conversations/{id}/read` | POST | Mark conversation as read |
| `/pet/conversations/read-all` | POST | Mark all as read |
| `/pet/conversations/{id}/summarize` | POST | AI-summarize a conversation |
| `/pet/summarize-all` | POST | AI-summarize all conversations |

## How It Works

1. The **iMessage Watcher** detects incoming messages and routes them through the **TamaBotchi Agent**
2. The agent responds via iMessage and logs the conversation to a local store
3. The **Desktop Pet** polls the agent API every 5 seconds for unread count
4. When you click the bunny, it opens the **Summary Panel** which shows all conversations
5. Clicking a conversation triggers **Claude AI** to generate a structured summary with who, intent, requirements, urgency, and action items
