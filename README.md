# team-ai

`team-ai` is a lightweight wrapper for Kimi CLI that generates team MCP configuration and supports direct RAGFlow MCP integration.

## What this does

- Loads team configuration from environment variables and env files.
- Generates `~/.team-ai/generated/mcp.json` safely.
- Supports direct RAGFlow MCP links via `TEAM_RAGFLOW_MCP_URL`.
- Supports direct RAG MCP links via `TEAM_RAG_MCP_URL`.
- Supports a local Gitea stdio adapter.
- Provides `doctor`, `mcp-json`, `run`, `login`, and `version` commands.

## Install

```bash
python -m pip install -e .
```

## Configuration

Create `~/.team-ai/team-ai.env` or export variables in your shell.

### RAGFlow MCP

```bash
TEAM_RAGFLOW_MCP_URL=https://ragflow.example.internal/mcp
TEAM_RAG_TOKEN=change-me
```

### Generic RAG MCP

```bash
TEAM_RAG_MCP_URL=https://rag.example.internal/mcp
TEAM_RAG_TOKEN=change-me
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

## Common issues

- `kimi` not found: install Kimi CLI and make sure it is on `PATH`.
- `--mcp-config-file` unsupported: your Kimi version may be too old.
- Gitea 401/403: check `GITEA_TOKEN` and `GITEA_AUTH_SCHEME`.
- RAGFlow connection failed: check `TEAM_RAGFLOW_MCP_URL`.

## Development

Run tests with:

```bash
python -m pytest -q
```
