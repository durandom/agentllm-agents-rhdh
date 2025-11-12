# AgentLLM RHDH Agents

RHDH-specific agents for AgentLLM, including ReleaseManager with Jira and Google Drive integration.

## Overview

This package provides agents specifically designed for RHDH (Red Hat Developer Hub) workflows:

- **ReleaseManager**: Agent for managing RHDH releases with Jira integration and Google Drive access

## Installation

```bash
pip install agentllm-agents-rhdh
```

Or with uv:

```bash
uv pip install agentllm-agents-rhdh
```

## Prerequisites

This package requires `agentllm-core` to be installed.

## Agents

### ReleaseManager

Release management assistant with integrated Jira and Google Drive toolkits.

**Features:**
- Jira issue tracking and queries
- Google Drive document access
- Extended system prompt from Google Docs
- Per-user credential management
- OAuth2 authentication flow

**Required Environment Variables:**
```bash
GEMINI_API_KEY=your_gemini_api_key
JIRA_SERVER_URL=https://your-jira-instance.atlassian.net
GDRIVE_CLIENT_ID=your_google_client_id
GDRIVE_CLIENT_SECRET=your_google_client_secret
```

**Optional Environment Variables:**
```bash
# URL or ID of Google Doc with extended system prompt
RELEASE_MANAGER_SYSTEM_PROMPT_GDRIVE_URL=https://docs.google.com/document/d/...
```

## Usage

### Via AgentLLM Proxy

The agent is automatically discovered when installed:

```yaml
# proxy_config.yaml (auto-generated)
model_list:
  - model_name: agno/release-manager
    litellm_params:
      model: agno/release-manager
      custom_llm_provider: agno
```

### Programmatic Usage

```python
from agentllm.agents.registry import AgentRegistry
from agentllm.db import TokenStorage
from agno.db.sqlite import SqliteDb

# Create infrastructure
db = SqliteDb(db_file="agents.db")
storage = TokenStorage(agno_db=db)

# Discover agents
registry = AgentRegistry()
registry.discover_agents()

# Get ReleaseManager factory
factory = registry.get_factory("release-manager")

# Create agent instance
agent = factory.create_agent(
    shared_db=db,
    token_storage=storage,
    user_id="user123",
    temperature=0.7,
)

# Use agent
response = await agent.arun("Show me release blockers")
print(response.content)
```

## Configuration Flow

### First Interaction

When a user first interacts with the ReleaseManager, they'll be prompted to configure required toolkits:

1. **Jira Configuration**: Provide API token for Jira access
2. **Google Drive Configuration**: Complete OAuth2 flow for Drive access

### Configuration Messages

**Jira:**
```
User: "Show me release blockers"
Agent: "To access Jira, please provide your API token..."
User: "My Jira API token is xxx"
Agent: "✅ Jira configured successfully!"
```

**Google Drive:**
```
User: "I want to access Google Drive"
Agent: "To access Google Drive, please authorize...
        Visit: https://accounts.google.com/o/oauth2/auth?...

        After authorization, provide the code."
User: "My authorization code is xxx"
Agent: "✅ Google Drive configured successfully!"
```

## Toolkit Configurations

### GoogleDriveConfig

Manages OAuth2 credentials for Google Drive access.

- **Type**: Required (prompts on first use)
- **Storage**: SQLite database via TokenStorage
- **Authentication**: OAuth2 authorization code flow

### JiraConfig

Manages API tokens for Jira access.

- **Type**: Required (prompts on first use)
- **Storage**: SQLite database via TokenStorage
- **Authentication**: API token

### SystemPromptExtensionConfig

Fetches extended system prompt from a Google Drive document.

- **Type**: Required (if RELEASE_MANAGER_SYSTEM_PROMPT_GDRIVE_URL is set)
- **Depends**: GoogleDriveConfig
- **Storage**: In-memory cache

## Tools

### GDriveTools

Google Drive integration toolkit providing:
- Document reading
- File listing
- Search capabilities

### JiraTools

Jira integration toolkit providing:
- Issue queries (JQL)
- Issue details
- Project information
- Sprint data

## Development

### Running Tests

```bash
# Install package with dev dependencies
uv pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Run with API key (for integration tests)
GEMINI_API_KEY=xxx pytest tests/ -v
```

### Testing Against Local agentllm-core

```bash
# Install agentllm-core in editable mode
cd ../agentllm-core
uv pip install -e .

# Install this package in editable mode
cd ../agentllm-agents-rhdh
uv pip install -e ".[dev]"

# Tests will use local agentllm-core
pytest tests/ -v
```

## Environment Variables Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `GEMINI_API_KEY` | Yes | Gemini API key for LLM access |
| `JIRA_SERVER_URL` | Yes | Jira server URL |
| `GDRIVE_CLIENT_ID` | Yes | Google OAuth2 client ID |
| `GDRIVE_CLIENT_SECRET` | Yes | Google OAuth2 client secret |
| `RELEASE_MANAGER_SYSTEM_PROMPT_GDRIVE_URL` | No | Google Doc URL/ID for extended prompt |

## Architecture

```
agentllm_agents_rhdh/
├── release_manager/
│   ├── agent.py          # ReleaseManager implementation
│   └── factory.py        # Factory for entry point
├── toolkit_configs/
│   ├── gdrive_config.py  # Google Drive configuration
│   ├── jira_config.py    # Jira configuration
│   └── system_prompt_extension_config.py
└── tools/
    ├── gdrive_toolkit.py # Google Drive tools
    ├── gdrive_utils.py   # OAuth utilities
    └── jira_toolkit.py   # Jira tools
```

## Related Documentation

- [Release Manager System Prompt Guide](https://github.com/yourorg/agentllm/blob/main/docs/release_manager_prompt_guide.md)
- [AgentLLM Core Documentation](https://github.com/yourorg/agentllm-core)

## License

MIT License - see [LICENSE](LICENSE) file for details.
