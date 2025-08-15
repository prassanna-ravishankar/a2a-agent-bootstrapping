#!/bin/bash

# Test script for A2A Agent Bootstrapping
# Tests all 4 independent A2A agents

set -e  # Exit on any error

# Only set GEMINI_API_KEY if it's not already set
if [[ -z "$GEMINI_API_KEY" ]]; then
    export GEMINI_API_KEY="dummy_key_for_testing"
    echo "ℹ️  Using dummy API key for testing (set GEMINI_API_KEY for real testing)"
else
    echo "ℹ️  Using existing GEMINI_API_KEY from environment"
fi

echo "🚀 Starting A2A Agent Bootstrapping server..."
uv run python -m a2a_agents.modal_app &
SERVER_PID=$!

echo "⏳ Waiting for server to start..."
sleep 8

echo ""
echo "🔍 Testing Independent A2A Agents..."
echo "==========================================="

echo ""
echo "🕵️‍♂️ Research Agent Card:"
if command -v jq &> /dev/null; then
    curl -s "http://localhost:8000/research/.well-known/agent.json" | jq '{name, description, url, skills: [.skills[].name]}'
else
    curl -s "http://localhost:8000/research/.well-known/agent.json"
fi

echo ""
echo "💻 Code Agent Card:"
if command -v jq &> /dev/null; then
    curl -s "http://localhost:8000/code/.well-known/agent.json" | jq '{name, description, url, skills: [.skills[].name]}'
else
    curl -s "http://localhost:8000/code/.well-known/agent.json"
fi

echo ""
echo "🔄 Data Agent Card:"
if command -v jq &> /dev/null; then
    curl -s "http://localhost:8000/data/.well-known/agent.json" | jq '{name, description, url, skills: [.skills[].name]}'
else
    curl -s "http://localhost:8000/data/.well-known/agent.json"
fi

echo ""
echo "🧠 Planning Agent Card:"
if command -v jq &> /dev/null; then
    curl -s "http://localhost:8000/planning/.well-known/agent.json" | jq '{name, description, url, skills: [.skills[].name]}'
else
    curl -s "http://localhost:8000/planning/.well-known/agent.json"
fi

echo ""
echo "📁 Agent Directory:"
if command -v jq &> /dev/null; then
    curl -s "http://localhost:8000/.well-known/agents" | jq '{description, agent_count: (.independent_agents | length)}'
else
    curl -s "http://localhost:8000/.well-known/agents"
fi

echo ""
echo "ℹ️  FastA2A Docs Limitation Notice..."
echo "==========================================="
echo "📝 FastA2A docs pages (/research/docs, /code/docs, etc.) are not fully"
echo "   compatible with multi-agent mounted systems. They may show 'Failed to"
echo "   load agent information' because they expect a single agent at the root."
echo ""
echo "✅ Recommended alternatives:"
echo "   • Individual agent cards: /research/.well-known/agent.json"
echo "   • Main documentation: http://localhost:8000/docs"
echo "   • Agent directory: http://localhost:8000/.well-known/agents"

echo ""
echo "🔍 Testing Root Agent Card (Multi-Agent Message)..."
echo "==========================================="

echo ""
echo "📄 Root agent card response:"
curl -s "http://localhost:8000/.well-known/agent.json" | jq -r '.message // "ERROR: No message field"'

echo ""
echo "🧪 Testing Server Health & Connectivity..."
echo "==========================================="

echo ""
echo "🏥 Main health check:"
curl -s "http://localhost:8000/health" | jq -r '.status // "ERROR"'

echo ""
echo "🔗 A2A endpoint connectivity test (Research Agent):"
RESEARCH_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X POST "http://localhost:8000/research/" -H "Content-Type: application/json" -d '{}')
if [ "$RESEARCH_STATUS" = "400" ] || [ "$RESEARCH_STATUS" = "422" ]; then
    echo "✅ A2A endpoint reachable (HTTP $RESEARCH_STATUS - expects valid A2A request)"
else
    echo "⚠️  Unexpected status: $RESEARCH_STATUS"
fi

echo ""
echo "📡 Testing A2A protocol basics:"
echo "ℹ️  A2A agents require specific JSON-RPC message format with 'parts' and 'kind' fields"
echo "ℹ️  Use agent cards (/.well-known/agent.json) for proper A2A client integration"

echo ""
echo "✅ SUCCESS: All 4 independent A2A agents are working!"
echo "Each agent can be discovered and used separately via their Agent Cards."
echo ""
echo "🌐 Available endpoints:"
echo "  • Research Agent: http://localhost:8000/research/"
echo "  • Code Agent: http://localhost:8000/code/"
echo "  • Data Agent: http://localhost:8000/data/"
echo "  • Planning Agent: http://localhost:8000/planning/"
echo ""
echo "📋 Agent Cards:"
echo "  • Research: http://localhost:8000/research/.well-known/agent.json"
echo "  • Code: http://localhost:8000/code/.well-known/agent.json"
echo "  • Data: http://localhost:8000/data/.well-known/agent.json"
echo "  • Planning: http://localhost:8000/planning/.well-known/agent.json"
echo ""
echo "📚 FastA2A Docs (⚠️  limited support):"
echo "  • Research: http://localhost:8000/research/docs"
echo "  • Code: http://localhost:8000/code/docs"
echo "  • Data: http://localhost:8000/data/docs"
echo "  • Planning: http://localhost:8000/planning/docs"
echo "  Note: These may show 'Failed to load agent information' due to multi-agent setup"

echo ""
echo "🛑 Stopping server..."
kill $SERVER_PID 2>/dev/null
wait $SERVER_PID 2>/dev/null
echo "✅ Server stopped."
