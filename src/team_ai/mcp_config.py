import json
import os
import stat
import sys
from pathlib import Path
from typing import Any

from team_ai.config import Settings


def _build_rag_server(url: str, token: str | None) -> dict[str, Any]:
    server: dict[str, Any] = {"url": url}
    if token:
        server["headers"] = {"Authorization": f"Bearer {token}"}
    return server


def build_mcp_config(settings: Settings) -> dict[str, Any]:
    mcp_servers: dict[str, Any] = {}
    if settings.rag_mcp_url:
        mcp_servers["team-rag"] = _build_rag_server(settings.rag_mcp_url, settings.rag_token)
    if settings.ragflow_mcp_url:
        mcp_servers["team-ragflow"] = _build_rag_server(settings.ragflow_mcp_url, settings.rag_token)
    if settings.gitea_base_url:
        env_vars = {
            "GITEA_BASE_URL": settings.gitea_base_url,
            "GITEA_TOKEN": settings.gitea_token or "",
            "GITEA_AUTH_SCHEME": settings.gitea_auth_scheme,
            "TEAM_AI_ENABLE_GITEA_WRITES": "1" if settings.enable_gitea_writes else "0",
        }
        mcp_servers["team-gitea"] = {
            "command": sys.executable,
            "args": ["-m", "team_ai.mcp.gitea_server"],
            "env": env_vars,
        }
    return {"mcpServers": mcp_servers}


def write_mcp_config(settings: Settings, destination: Path) -> Path:
    settings.generated_dir.mkdir(parents=True, exist_ok=True)
    config = build_mcp_config(settings)
    destination.write_text(json.dumps(config, indent=2, ensure_ascii=False))
    destination.chmod(stat.S_IRUSR | stat.S_IWUSR)
    return destination
