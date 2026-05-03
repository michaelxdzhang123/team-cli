#!/usr/bin/env bash
# Test script for RAGFlow MCP configuration
# Usage: ./test_ragflow.sh

set -e

echo "🧪 Testing RAGFlow MCP Configuration"
echo "====================================="

# Check if environment variables are set
if [ -z "$TEAM_RAGFLOW_MCP_URL" ] && [ -z "$TEAM_AI_ENABLE_LOCAL_RAGFLOW" ]; then
    echo "❌ TEAM_RAGFLOW_MCP_URL is not set"
    echo "   Please set it to your RAGFlow MCP endpoint URL or enable local RAGFlow"
    echo "   Example: export TEAM_AI_ENABLE_LOCAL_RAGFLOW=1"
    exit 1
fi

if [ -z "$TEAM_RAG_TOKEN" ] && [ -z "$TEAM_AI_ENABLE_LOCAL_RAGFLOW" ]; then
    echo "❌ TEAM_RAG_TOKEN is not set"
    echo "   Please set it to your actual RAGFlow token when using remote RAGFlow"
    exit 1
fi

echo "✅ Environment variables are set"
if [ -n "$TEAM_RAGFLOW_MCP_URL" ]; then
    echo "   TEAM_RAGFLOW_MCP_URL: $TEAM_RAGFLOW_MCP_URL"
fi
if [ -n "$TEAM_AI_ENABLE_LOCAL_RAGFLOW" ]; then
    echo "   TEAM_AI_ENABLE_LOCAL_RAGFLOW: $TEAM_AI_ENABLE_LOCAL_RAGFLOW"
fi
if [ -n "$TEAM_RAG_TOKEN" ]; then
    echo "   TEAM_RAG_TOKEN: [REDACTED]"
fi

# Run doctor command
echo ""
echo "🔍 Running team-ai doctor..."
uv run --group dev python -m team_ai.cli doctor

# Generate and show MCP config
echo ""
echo "📄 Generated MCP configuration (redacted):"
uv run --group dev python -m team_ai.cli mcp-json --print | jq . 2>/dev/null || uv run --group dev python -m team_ai.cli mcp-json --print

echo ""
echo "🎉 RAGFlow MCP configuration test completed!"
echo ""
echo "Next steps:"
echo "1. Run: team-ai run 'Test your RAGFlow integration'"
echo "2. Verify that RAGFlow tools are available in Kimi"
echo "3. Test actual RAG queries through the MCP interface"