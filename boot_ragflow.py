#!/usr/bin/env python3
"""
RAGFlow MCP Server Launcher
Provides both stdio and HTTP server modes for the RAGFlow MCP server.
"""

import argparse
import os
import sys
from pathlib import Path

def run_stdio_server():
    """Run the RAGFlow MCP server in stdio mode."""
    print("🚀 Starting RAGFlow MCP Server (stdio mode)...", file=sys.stderr)
    os.execvp(sys.executable, [sys.executable, str(Path(__file__).parent / "ragflow_server.py")])

def run_http_server(port: int = 8000, host: str = "localhost"):
    """Run the RAGFlow MCP server as an HTTP server."""
    print(f"🌐 Starting RAGFlow MCP HTTP Server on http://{host}:{port}...", file=sys.stderr)

    # Import here to avoid import errors if fastmcp is not available
    from fastmcp import FastMCP
    import uvicorn

    # Import the app from ragflow_server.py
    sys.path.insert(0, str(Path(__file__).parent))
    from ragflow_server import app

    # Get the HTTP app from FastMCP
    asgi_app = app.http_app

    # Run with uvicorn
    uvicorn.run(asgi_app, host=host, port=port)

def main():
    parser = argparse.ArgumentParser(description="RAGFlow MCP Server Launcher")
    parser.add_argument(
        "--mode",
        choices=["stdio", "http"],
        default="stdio",
        help="Server mode (default: stdio)"
    )
    parser.add_argument(
        "--host",
        default="localhost",
        help="HTTP server host (default: localhost)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="HTTP server port (default: 8000)"
    )

    args = parser.parse_args()

    if args.mode == "stdio":
        run_stdio_server()
    elif args.mode == "http":
        run_http_server(args.port, args.host)

if __name__ == "__main__":
    main()