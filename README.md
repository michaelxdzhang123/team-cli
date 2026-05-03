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

This project includes a simple RAGFlow MCP server for testing and development:

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
