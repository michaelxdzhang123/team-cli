import os
from pathlib import Path

from team_ai.config import Settings


def test_settings_loads_from_env(tmp_path: Path, monkeypatch: object) -> None:
    # Clear any existing env vars that might interfere
    monkeypatch.delenv("TEAM_RAGFLOW_MCP_URL", raising=False)
    monkeypatch.delenv("TEAM_RAG_MCP_URL", raising=False)
    monkeypatch.delenv("TEAM_RAG_TOKEN", raising=False)

    env_file = tmp_path / "team-ai.env"
    env_file.write_text("TEAM_AI_HOME=~/my-team-ai\nTEAM_RAGFLOW_MCP_URL=https://ragflow.example/mcp\nTEAM_RAG_TOKEN=secret123\n")
    monkeypatch.setenv("TEAM_AI_ENV_FILE", str(env_file))
    settings = Settings.from_env(Path.cwd())
    assert str(settings.team_ai_home).endswith("my-team-ai")
    assert settings.ragflow_mcp_url == "https://ragflow.example/mcp"
    assert settings.rag_token == "secret123"


def test_validate_for_mcp_creates_directories(tmp_path: Path, monkeypatch: object) -> None:
    monkeypatch.setenv("TEAM_AI_HOME", str(tmp_path / "team-ai"))
    settings = Settings.from_env(Path.cwd())
    settings.validate_for_mcp()
    assert settings.team_ai_home.exists()
    assert settings.generated_dir.exists()


def test_invalid_gitea_scheme_raises(tmp_path: Path, monkeypatch: object) -> None:
    monkeypatch.setenv("GITEA_AUTH_SCHEME", "unknown")
    settings = Settings.from_env(Path.cwd())
    try:
        settings.validate_for_mcp()
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert "GITEA_AUTH_SCHEME" in str(exc)
