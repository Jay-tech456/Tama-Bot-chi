# TLDR

This folder implements tools for gmail and google calendar access, sending emails and stuff


# MCP Gmail Server

A Model Context Protocol (MCP) server that provides Gmail access for LLMs, powered by the [MCP Python SDK](https://github.com/mod<elcontextprotocol/python-sdk).

## Features

- Expose Gmail messages as MCP resources
- Provide tools for composing, sending, and managing emails
- OAuth 2.0 authentication with Google's Gmail API

## Prerequisites

- Python 3.10+
- Gmail account with API access
- [uv](https://github.com/astral-sh/uv) for Python package management (recommended)

## Setup

### 1. Install dependencies

Install project dependencies (uv automatically creates and manages a virtual environment)
```bash
uv sync
```

### 2. Configure Gmail OAuth credentials

There's unfortunately a lot of steps required to use the Gmail API. I've attempted to capture all of the required steps (as of March 28, 2025) but things may change.

#### Google Cloud Setup

1. **Create a Google Cloud Project**
    - Go to [Google Cloud Console](https://console.cloud.google.com/)
    - Click on the project dropdown at the top of the page
    - Click "New Project"
    - Enter a project name (e.g., "MCP Gmail Integration")
    - Click "Create"
    - Wait for the project to be created and select it from the dropdown

2. **Enable the Gmail API**
    - In your Google Cloud project, go to the navigation menu (≡)
    - Select "APIs & Services" > "Library"
    - Search for "Gmail API"
    - Click on the Gmail API card
    - Click "Enable"

3. **Configure OAuth Consent Screen**
    - Go to "APIs & Services" > "OAuth consent screen"
    - You will likely see something like "Google Auth Platform not configured yet"
        - Click on "Get started"
    - Fill in the required application information:
        - App name: "MCP Gmail Integration"
        - User support email: Your email address
    - Fill in the required audience information:
        - Choose "External" user type (unless you have a Google Workspace organization)
    - Fill in the required contact information:
        - Your email address
    - Click "Save and Continue"
   - Click "Create"

4. **Create OAuth Credentials**
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Choose "Desktop app" as the application type
   - Enter a name (e.g., "MCP Gmail Desktop Client")
   - Click "Create"
   - Click "Download JSON" for the credentials you just created
   - Save the file as `credentials.json` in your project root directory

5. **Add scopes**
    - Go to "APIs & Services" > "OAuth consent screen"
    - Go to the "Data Access" tab
    - Click "Add or remove scopes"
    - Search for the Gmail API
    - Select the scope for `.../auth/gmail.modify` which grants permission to "Read, compose, and send emails from your Gmail account"
    - Click update
    - Click save

Verify that you've set up your OAuth configuration correctly by running a simple test script.

```bash
uv run python scripts/test_gmail_setup.py
```

You should be able to see usage metrics at https://console.cloud.google.com/apis/api/gmail.googleapis.com/metrics

### 3. Run the server

Development mode:
```bash
uv run mcp dev mcp_gmail/server.py
```
This will launch an mcp server at http://127.0.0.1:8090/sse,
You can test it out with mcp inspector,

Or install for use with Claude Desktop:
```bash
uv run mcp install \
    --with-editable .
    --name gmail \
    --env-var MCP_GMAIL_CREDENTIALS_PATH=$(pwd)/credentials.json \
    --env-var MCP_GMAIL_TOKEN_PATH=$(pwd)/token.json \
    mcp_gmail/server.py
```

> [!NOTE]
> If you encounter an error like `Error: spawn uv ENOENT` when spinning up Claude Desktop and initializing the MCP server, you may need to update your `claude_desktop_config.json` to provide the **absolute** path to `uv`. Go to Claude Desktop -> Settings -> Developer -> Edit Config.
>
> ```json
> {
>   "mcpServers": {
>     "gmail": {
>       "command": "~/.local/bin/uv",
>     }
>   }
> }
> ```

## Development

### Linting and Testing

Run linting and formatting:
```bash
# Format code
uv run ruff format .

# Lint code with auto-fixes where possible
uv run ruff check --fix .

# Run tests
uv run pytest tests/
```

### Pre-commit Hooks

This project uses pre-commit hooks to ensure code quality. The hooks automatically run before each commit to verify code formatting and linting standards.

Install the pre-commit hooks:
```bash
pre-commit install
```

Run pre-commit manually on all files:
```bash
pre-commit run --all-files
```

## Usage

Once running, you can connect to the MCP server using any MCP client or via Claude Desktop.

### Available Resources

- `gmail://messages/{message_id}` - Access email messages
- `gmail://threads/{thread_id}` - Access email threads

### Available Tools

- `compose_email` - Create a new email draft
- `send_email` - Send an email
- `search_emails` - Search for emails with specific filters (from, to, subject, dates, etc.)
- `query_emails` - Search for emails using raw Gmail query syntax
- `get_emails` - Retrieve multiple email messages by their IDs
- `list_available_labels` - Get all available Gmail labels
- `mark_message_read` - Mark a message as read
- `add_label_to_message` - Add a label to a message
- `remove_label_from_message` - Remove a label from a message

## Environment Variables

You can configure the server using environment variables:

- `MCP_GMAIL_CREDENTIALS_PATH`: Path to the OAuth credentials JSON file (default: "credentials.json")
- `MCP_GMAIL_TOKEN_PATH`: Path to store the OAuth token (default: "token.json")
- `MCP_GMAIL_MAX_RESULTS`: Default maximum results for search queries (default: 10)

## License

MIT
