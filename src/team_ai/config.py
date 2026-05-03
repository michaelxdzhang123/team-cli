import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any


def _load_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def _env_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on", "y"}


@dataclass(frozen=True)
class Settings:
    team_ai_home: Path
    kimi_share_dir: Path
    generated_dir: Path
    gitea_base_url: str | None
    gitea_token: str | None
    gitea_auth_scheme: str
    enable_gitea_writes: bool
    rag_mcp_url: str | None
    ragflow_mcp_url: str | None
    rag_api_base: str | None
    rag_token: str | None
    rag_search_path: str
    rag_doc_path: str
    rag_search_method: str
    enable_local_ragflow: bool

    @classmethod
    def from_env(cls, project_root: Path) -> "Settings":
        env = dict(os.environ)
        env_file_path = Path(env.get("TEAM_AI_ENV_FILE", "")).expanduser() if env.get("TEAM_AI_ENV_FILE") else None
        if env_file_path and env_file_path.exists():
            env = {**_load_env_file(env_file_path), **env}
        else:
            candidate = Path.home() / ".team-ai" / "team-ai.env"
            if candidate.exists():
                env = {**_load_env_file(candidate), **env}
            else:
                fallback = project_root / ".env"
                if fallback.exists():
                    env = {**_load_env_file(fallback), **env}

        team_ai_home = Path(env.get("TEAM_AI_HOME", "~/.team-ai")).expanduser()
        kimi_share_dir = Path(env.get("KIMI_SHARE_DIR", str(team_ai_home / "kimi"))).expanduser()
        generated_dir = team_ai_home / "generated"

        return cls(
            team_ai_home=team_ai_home,
            kimi_share_dir=kimi_share_dir,
            generated_dir=generated_dir,
            gitea_base_url=env.get("GITEA_BASE_URL"),
            gitea_token=env.get("GITEA_TOKEN"),
            gitea_auth_scheme=(env.get("GITEA_AUTH_SCHEME") or "token").strip().lower(),
            enable_gitea_writes=_env_bool(env.get("TEAM_AI_ENABLE_GITEA_WRITES"), False),
            rag_mcp_url=env.get("TEAM_RAG_MCP_URL"),
            ragflow_mcp_url=env.get("TEAM_RAGFLOW_MCP_URL"),
            rag_api_base=env.get("TEAM_RAG_API_BASE"),
            rag_token=env.get("TEAM_RAG_TOKEN"),
            rag_search_path=env.get("TEAM_RAG_SEARCH_PATH", "/search"),
            rag_doc_path=env.get("TEAM_RAG_DOC_PATH", "/doc"),
            rag_search_method=env.get("TEAM_RAG_SEARCH_METHOD", "POST").upper(),
            enable_local_ragflow=_env_bool(env.get("TEAM_AI_ENABLE_LOCAL_RAGFLOW"), False),
        )

    def validate_for_mcp(self) -> None:
        self.team_ai_home.mkdir(parents=True, exist_ok=True)
        self.kimi_share_dir.mkdir(parents=True, exist_ok=True)
        self.generated_dir.mkdir(parents=True, exist_ok=True)
        if self.gitea_auth_scheme not in {"token", "bearer"}:
            raise ValueError("GITEA_AUTH_SCHEME must be 'token' or 'bearer'.")
        if self.rag_search_method not in {"GET", "POST"}:
            raise ValueError("TEAM_RAG_SEARCH_METHOD must be GET or POST.")

    def redacted(self) -> dict[str, Any]:
        return {
            "team_ai_home": str(self.team_ai_home),
            "kimi_share_dir": str(self.kimi_share_dir),
            "gitea_base_url": self.gitea_base_url,
            "gitea_token": "set" if self.gitea_token else "missing",
            "gitea_auth_scheme": self.gitea_auth_scheme,
            "enable_gitea_writes": self.enable_gitea_writes,
            "rag_mcp_url": self.rag_mcp_url,
            "ragflow_mcp_url": self.ragflow_mcp_url,
            "rag_api_base": self.rag_api_base,
            "rag_token": "set" if self.rag_token else "missing",
            "rag_search_path": self.rag_search_path,
            "rag_doc_path": self.rag_doc_path,
            "rag_search_method": self.rag_search_method,
        }
