#!/usr/bin/env python3
"""
Test script for the RAGFlow MCP server.
"""

import asyncio
import json
import subprocess
import sys
import time
from pathlib import Path

async def test_stdio_server():
    """Test the stdio mode of the RAGFlow server."""
    print("🧪 Testing RAGFlow MCP Server (stdio mode)...")

    # Start the server in a subprocess
    server_process = subprocess.Popen(
        [sys.executable, str(Path(__file__).parent / "ragflow_server.py")],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    try:
        # Wait a bit for server to start
        time.sleep(2)

        # Send initialize request
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }

        server_process.stdin.write(json.dumps(init_request) + "\n")
        server_process.stdin.flush()

        # Read response
        response_line = server_process.stdout.readline().strip()
        if response_line:
            response = json.loads(response_line)
            print(f"✅ Server initialized: {response.get('result', {}).get('serverInfo', {}).get('name', 'unknown')}")

        # Test tools/list
        tools_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }

        server_process.stdin.write(json.dumps(tools_request) + "\n")
        server_process.stdin.flush()

        tools_response_line = server_process.stdout.readline().strip()
        if tools_response_line:
            tools_response = json.loads(tools_response_line)
            tools = tools_response.get('result', {}).get('tools', [])
            print(f"✅ Found {len(tools)} tools: {[t.get('name') for t in tools]}")

        # Test rag_search tool
        search_request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "rag_search",
                "arguments": {
                    "query": "AI",
                    "top_k": 2
                }
            }
        }

        server_process.stdin.write(json.dumps(search_request) + "\n")
        server_process.stdin.flush()

        search_response_line = server_process.stdout.readline().strip()
        if search_response_line:
            search_response = json.loads(search_response_line)
            results = search_response.get('result', {}).get('content', [{}])[0].get('text', '{}')
            results_data = json.loads(results)
            print(f"✅ Search returned {len(results_data.get('results', []))} results")

        print("🎉 Stdio server test completed successfully!")

    finally:
        server_process.terminate()
        server_process.wait()

async def test_http_server():
    """Test the HTTP mode of the RAGFlow server."""
    print("🌐 Testing RAGFlow MCP Server (HTTP mode)...")

    # Import here to avoid issues if not available
    try:
        import httpx
    except ImportError:
        print("❌ httpx not available, skipping HTTP test")
        return

    # Start HTTP server in background
    server_process = subprocess.Popen([
        sys.executable, str(Path(__file__).parent / "boot_ragflow.py"),
        "--mode", "http", "--port", "8002", "--host", "localhost"
    ])

    try:
        # Wait for server to start
        time.sleep(3)

        async with httpx.AsyncClient() as client:
            # Test server is running
            response = await client.get("http://localhost:8002/docs")
            if response.status_code == 200:
                print("✅ HTTP server is running and accessible")
            else:
                print(f"⚠️  HTTP server responded with status {response.status_code}")

        print("🎉 HTTP server test completed!")

    finally:
        server_process.terminate()
        server_process.wait()

async def main():
    """Run all tests."""
    print("🚀 Starting RAGFlow MCP Server Tests\n")

    await test_stdio_server()
    print()
    await test_http_server()

    print("\n✅ All tests completed!")

if __name__ == "__main__":
    asyncio.run(main())