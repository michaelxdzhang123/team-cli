import json
from pathlib import Path

from team_ai.config import Settings
from team_ai.mcp_config import build_mcp_config, write_mcp_config


def test_build_mcp_config_includes_ragflow_and_gitea(tmp_path: Path, monkeypatch: object) -> None:
    monkeypatch.setenv("TEAM_AI_HOME", str(tmp_path / "team-ai"))
    monkeypatch.setenv("TEAM_RAGFLOW_MCP_URL", "https://ragflow.example/mcp")
    monkeypatch.setenv("TEAM_RAG_TOKEN", "secret-abc")
    monkeypatch.setenv("GITEA_BASE_URL", "https://gitea.example")
    monkeypatch.setenv("GITEA_TOKEN", "gitea-token")

    settings = Settings.from_env(Path.cwd())
    config = build_mcp_config(settings)

    assert config["mcpServers"]["team-ragflow"]["url"] == "https://ragflow.example/mcp"
    assert config["mcpServers"]["team-ragflow"]["headers"]["Authorization"] == "Bearer secret-abc"
    assert config["mcpServers"]["team-gitea"]["command"]
    assert config["mcpServers"]["team-gitea"]["env"]["GITEA_AUTH_SCHEME"] == "token"


def test_write_mcp_config_writes_json(tmp_path: Path, monkeypatch: object) -> None:
    monkeypatch.setenv("TEAM_AI_HOME", str(tmp_path / "team-ai"))
    monkeypatch.setenv("TEAM_RAGFLOW_MCP_URL", "https://ragflow.example/mcp")
    monkeypatch.setenv("TEAM_RAG_TOKEN", "secret-abc")
    settings = Settings.from_env(Path.cwd())
    settings.validate_for_mcp()
    destination = settings.generated_dir / "mcp.json"
    written = write_mcp_config(settings, destination)
    assert written.exists()

    data = json.loads(written.read_text())
    assert data["mcpServers"]["team-ragflow"]["url"] == "https://ragflow.example/mcp"
    assert written.stat().st_mode & 0o777 == 0o600
