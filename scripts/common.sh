#!/bin/bash
# Shared shell helpers for ACAT-X automation

set -euo pipefail

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

print_header() {
  echo ""
  echo -e "${BLUE}========================================${NC}"
  echo -e "${BLUE}  $1${NC}"
  echo -e "${BLUE}========================================${NC}"
  echo ""
}

print_success() { echo -e "${GREEN}✅ $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
print_phase() { echo -e "${CYAN}→ $1${NC}"; }

check_ollama() {
  if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama not installed"
    exit 1
  fi
  if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "❌ Ollama service not running"
    echo "Start with: ollama serve"
    exit 1
  fi
  print_success "Ollama is running"
}

check_model_available() {
  local model_name=$1
  ollama ls | grep -q "$model_name"
}
