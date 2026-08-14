#!/bin/bash
# Fast ACAT-X Benchmark using lightweight evaluator (no Inspect AI overhead)

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Configuration
MODELS=("ollama/phi" "ollama/mistral")
DIMENSIONS=("consist" "truth")
SAMPLES_PER_TEST=3

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_header() {
    echo ""
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Check Ollama
print_header "Checking Ollama"

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

# Check models
print_header "Checking Models"

for model in "${MODELS[@]}"; do
    model_name=${model##*/}
    if ollama ls | grep -q "$model_name"; then
        print_success "$model_name available"
    else
        print_warning "$model_name not found"
    fi
done

# Run benchmarks
print_header "Running Fast Benchmarks"

total=$((${#MODELS[@]} * ${#DIMENSIONS[@]}))
current=0

for model in "${MODELS[@]}"; do
    model_name=${model##*/}
    echo ""
    echo -e "${BLUE}Testing: $model_name${NC}"

    for dimension in "${DIMENSIONS[@]}"; do
        ((current++))
        echo -n "  [$current/$total] $dimension ... "

        if uv run python lightweight_eval.py "$dimension" "$model" "$SAMPLES_PER_TEST" > /dev/null 2>&1; then
            print_success "Done"
        else
            print_warning "Failed"
        fi
    done
done

# Summary
print_header "Results Summary"

echo "Results saved to: results/lightweight_*.json"
echo ""
echo "View results with:"
echo "  cat results/lightweight_*.json | jq '.stats'"
echo ""
echo "Compare models:"
echo "  python -c \"import json; results = [json.load(open(f)) for f in __import__('glob').glob('results/lightweight_*.json')]; [print(f\\\"{r['model']} {r['dimension']}: {r['stats']['average']:.3f}\\\") for r in results]\""
echo ""

print_success "Benchmark complete!"
