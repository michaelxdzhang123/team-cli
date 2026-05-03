# team-ai

`team-ai` is a lightweight wrapper for Kimi CLI that generates team MCP configuration and supports direct RAGFlow MCP integration.

## What this does

- Loads team configuration from environment variables and env files.
- Generates `~/.team-ai/generated/mcp.json` safely.
- Supports direct RAGFlow MCP links via `TEAM_RAGFLOW_MCP_URL`.
- Supports direct RAG MCP links via `TEAM_RAG_MCP_URL`.
- **NEW**: Includes a local RAGFlow MCP server for testing and development.
- Supports a local Gitea stdio adapter.
- Provides `doctor`, `mcp-json`, `run`, `login`, and `version` commands.

## Install

### Using uv (recommended)

```bash
# Install with development dependencies (includes fastmcp for MCP server)
uv sync --group dev

# Or install without dev dependencies
uv sync
```

### Using pip

```bash
python -m pip install -e .
```

## Local RAGFlow MCP Server

This project includes a simple RAGFlow MCP server for testing and development.

> For integrated local usage with `team-ai`, see the section below:
> [Using the Integrated RAGFlow Server](#using-the-integrated-ragflow-server)

### Start the server (stdio mode)

```bash
# Run in stdio mode (for direct MCP integration)
uv run python ragflow_server.py
```

### Start the server (HTTP mode)

```bash
# Run as HTTP server on port 8000
uv run python boot_ragflow.py --mode http --port 8000

# Or use the launcher script
python boot_ragflow.py --mode http --host 0.0.0.0 --port 8001
```

### Test the server

```bash
# Test stdio mode with MCP client
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/list"}' | uv run python ragflow_server.py

# Test HTTP mode (server provides MCP over HTTP)
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}'
```

### Available tools

- `rag_search(query, repo?, top_k?)` - Search documents
- `rag_get_doc(doc_id)` - Get specific document
- `rag_answer_with_sources(question, repo?)` - Answer with sources

## Configuration

Create `~/.team-ai/team-ai.env` or export variables in your shell.

### RAGFlow MCP

```bash
TEAM_RAGFLOW_MCP_URL=https://ragflow.example.internal/mcp
TEAM_RAG_TOKEN=your-actual-token-here
```

### Generic RAG MCP

```bash
TEAM_RAG_MCP_URL=https://rag.example.internal/mcp
TEAM_RAG_TOKEN=your-actual-token-here
```

### Local RAGFlow Server

For testing with the local server:

```bash
# Use local HTTP server
TEAM_RAGFLOW_MCP_URL=http://localhost:8000/mcp

# Or use stdio mode (configure in team-ai.env)
# TEAM_RAGFLOW_MCP_URL=stdio://python ragflow_server.py
```

### Gitea adapter

```bash
GITEA_BASE_URL=https://gitea.example.internal
GITEA_TOKEN=change-me
GITEA_AUTH_SCHEME=token
TEAM_AI_ENABLE_GITEA_WRITES=0
```

### Team directories

```bash
TEAM_AI_HOME=~/.team-ai
KIMI_SHARE_DIR=~/.team-ai/kimi
```

## Running

```bash
team-ai doctor
team-ai mcp-json --print
team-ai run --help
```

## Using the Integrated RAGFlow Server

The local RAGFlow MCP server can be automatically integrated into team-ai:

### Enable local RAGFlow

Option 1: Via environment variable
```bash
export TEAM_AI_ENABLE_LOCAL_RAGFLOW=1
```

Option 2: Via config file (`~/.team-ai/team-ai.env`)
```bash
TEAM_AI_ENABLE_LOCAL_RAGFLOW=1
```

### Verify integration

```bash
# Check status
team-ai doctor

# You should see: rag_mode: local_ragflow
```

### View MCP configuration

```bash
# Shows the generated MCP config including the local RAGFlow server
team-ai mcp-json --print
```

### Use with Kimi CLI

```bash
# Query the local RAGFlow database
team-ai run "What do we know about AI?"

# The RAGFlow tools will be available:
# - rag_search: Search documents
# - rag_get_doc: Get specific document
# - rag_answer_with_sources: Answer with source citations
```

### Combining with remote RAGFlow

You can use both local and remote RAGFlow servers simultaneously:

```bash
export TEAM_AI_ENABLE_LOCAL_RAGFLOW=1
export TEAM_RAGFLOW_MCP_URL=https://remote-ragflow.example.com/mcp
export TEAM_RAG_TOKEN=your-token

# MCP config will include both:
# - team-ragflow-local (stdio server)
# - team-ragflow (HTTP remote server)
team-ai run "Query both local and remote RAGFlow"
```

### Testing RAGFlow MCP Configuration

To verify your RAGFlow MCP setup:

```bash
# Set environment variables
export TEAM_RAGFLOW_MCP_URL="https://your-ragflow-instance.com/mcp"
export TEAM_RAG_TOKEN="your-actual-token"

# Run the automated test script
./test_ragflow.sh

# Or test manually:
# Check configuration
team-ai doctor

# View generated MCP config (tokens redacted)
team-ai mcp-json --print

# Test with Kimi CLI
team-ai run "Test RAGFlow integration"
```

## Common issues

- `kimi` not found: install Kimi CLI and make sure it is on `PATH`.
- `--mcp-config-file` unsupported: your Kimi version may be too old.
- Gitea 401/403: check `GITEA_TOKEN` and `GITEA_AUTH_SCHEME`.
- RAGFlow connection failed: check `TEAM_RAGFLOW_MCP_URL`.

## Development

After installation, run tests with:

```bash
# Using uv (recommended)
uv run --group dev pytest -q

# Or using pytest directly
python -m pytest -q
```
