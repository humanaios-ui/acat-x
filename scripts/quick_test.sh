#!/bin/bash
# ACAT-X Quick Test Setup Script
# Verifies dependencies and runs a test evaluation

set -e

echo "=========================================="
echo "ACAT-X Quick Test Setup"
echo "=========================================="
echo ""

# Check Python/uv
echo "1. Checking Python environment..."
if ! command -v uv &> /dev/null; then
    echo "   ❌ uv not found. Install from https://docs.astral.sh/uv/"
    exit 1
fi
echo "   ✅ uv is available"

# Check Inspect AI
echo ""
echo "2. Checking Inspect AI installation..."
if ! uv run python -c "import inspect_ai" &> /dev/null; then
    echo "   ⚠️  Inspect AI not found, installing..."
    uv pip install inspect-ai
fi
echo "   ✅ Inspect AI is available"

# Check OpenAI dependency (required for Ollama)
echo ""
echo "3. Checking OpenAI dependency (required for Ollama)..."
if ! uv run python -c "import openai" &> /dev/null; then
    echo "   ⚠️  openai not found, installing..."
    uv pip install openai
fi
echo "   ✅ OpenAI dependency is available"

# Check Ollama
echo ""
echo "4. Checking Ollama..."
if ! command -v ollama &> /dev/null; then
    echo "   ❌ Ollama not found"
    echo "   Install from: https://ollama.com/download"
    echo "   Mac (Homebrew): brew install ollama"
    echo "   Then: brew services start ollama"
    exit 1
fi
echo "   ✅ Ollama is installed"

# Check if Ollama is running
echo ""
echo "5. Checking if Ollama service is running..."
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "   ❌ Ollama API not responding on localhost:11434"
    echo "   Start Ollama with: ollama serve"
    echo "   (or: brew services start ollama)"
    exit 1
fi
echo "   ✅ Ollama is running"

# Check for a model
echo ""
echo "6. Checking for available models..."
MODELS=$(uv run python -c "import requests; r=requests.get('http://localhost:11434/api/tags'); import json; data=json.loads(r.text); print([m['model'] for m in data['models']])")

if echo "$MODELS" | grep -q "llama2\|mistral"; then
    echo "   ✅ Found models: $MODELS"
else
    echo "   ⚠️  No suitable models found"
    echo "   Pull a model with:"
    echo "     ollama pull llama2:7b"
    echo "     ollama pull mistral"
    exit 1
fi

# Ready to test
echo ""
echo "=========================================="
echo "Setup Complete! Ready to test."
echo "=========================================="
echo ""
echo "Run a quick evaluation:"
echo ""
echo "  cd $(pwd)"
echo "  uv run inspect eval src/acat_x/consist --model ollama/llama2:7b --log-dir results/quick_test"
echo ""
echo "Or with Mistral:"
echo ""
echo "  uv run inspect eval src/acat_x/consist --model ollama/mistral --log-dir results/quick_test"
echo ""
