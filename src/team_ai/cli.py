import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Sequence

from team_ai.config import Settings
from team_ai.mcp_config import build_mcp_config, write_mcp_config
from team_ai.redaction import redact_secret


def _find_kimi() -> str | None:
    return shutil.which("kimi")


def _run_kimi_cli(kimi_path: str, mcp_path: Path, args: Sequence[str]) -> int:
    cmd = [kimi_path, "--mcp-config-file", str(mcp_path), *args]
    result = subprocess.run(cmd, env=None)
    return result.returncode


def _print_doctor(settings: Settings, args: argparse.Namespace) -> None:
    python_path = sys.executable
    print(f"python_version: {sys.version.split()[0]}")
    print(f"python_executable: {python_path}")
    kimi_path = _find_kimi()
    print(f"kimi_found: {bool(kimi_path)}")
    if kimi_path:
        print(f"kimi_path: {kimi_path}")
    else:
        print("kimi_path: missing")

    if kimi_path:
        help_text = subprocess.run([kimi_path, "--help"], capture_output=True, text=True)
        supports_mcp = "--mcp-config-file" in help_text.stdout
        print(f"kimi_supports_mcp_config_file: {supports_mcp}")
    else:
        print("kimi_supports_mcp_config_file: false")

    print(f"TEAM_AI_HOME: {settings.team_ai_home}")
    print(f"KIMI_SHARE_DIR: {settings.kimi_share_dir}")
    if settings.ragflow_mcp_url:
        print("rag_mode: ragflow_mcp_url")
    elif settings.rag_mcp_url:
        print("rag_mode: rag_mcp_url")
    elif settings.rag_api_base:
        print("rag_mode: rag_api_base")
    else:
        print("rag_mode: none")
    print(f"gitea_base_url: {'set' if settings.gitea_base_url else 'missing'}")
    print(f"gitea_token: {'set' if settings.gitea_token else 'missing'}")
    mcp_path = settings.generated_dir / "mcp.json"
    print(f"generated_mcp_path: {mcp_path}")
    print(f"generated_dir_exists: {settings.generated_dir.exists()}")

    if args.check_network:
        print("network_check: skipped by default")


def _load_settings() -> Settings:
    settings = Settings.from_env(Path.cwd())
    settings.validate_for_mcp()
    return settings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="team-ai")
    subparsers = parser.add_subparsers(dest="command")

    doctor_parser = subparsers.add_parser("doctor", help="Show environment and MCP health checks")
    doctor_parser.add_argument("--check-network", action="store_true", help="Enable network checks")

    mcp_parser = subparsers.add_parser("mcp-json", help="Generate MCP JSON")
    mcp_parser.add_argument("--print", action="store_true", help="Print redacted MCP JSON")

    run_parser = subparsers.add_parser("run", help="Run Kimi with generated MCP config")
    run_parser.add_argument("--", dest="separator", nargs="?", help="Delimiter before Kimi args")
    run_parser.add_argument("args", nargs=argparse.REMAINDER, help="Arguments forwarded to Kimi")

    subparsers.add_parser("login", help="Run Kimi login or show instructions")
    subparsers.add_parser("version", help="Show team-ai version")

    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return 1

    settings = _load_settings()
    mcp_path = write_mcp_config(settings, settings.generated_dir / "mcp.json")

    if args.command == "doctor":
        _print_doctor(settings, args)
        return 0
    if args.command == "mcp-json":
        if args.print:
            print(json.dumps(redact_secret(json.dumps(build_mcp_config(settings)), [settings.rag_token or "", settings.gitea_token or ""]), indent=2))
        return 0
    if args.command == "run":
        kimi_path = _find_kimi()
        if not kimi_path:
            print("Error: kimi not found on PATH. Install Kimi CLI and retry.")
            return 2
        return _run_kimi_cli(kimi_path, mcp_path, args.args or [])
    if args.command == "login":
        kimi_path = _find_kimi()
        if not kimi_path:
            print("Error: kimi not found on PATH. Install Kimi CLI and retry.")
            return 2
        help_text = subprocess.run([kimi_path, "--help"], capture_output=True, text=True)
        if "login" in help_text.stdout:
            return subprocess.run([kimi_path, "login"]).returncode
        print("Kimi login is not available in this version. Run `team-ai run` and follow the Kimi login instructions.")
        return 0
    if args.command == "version":
        from team_ai import __version__

        print(__version__)
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
