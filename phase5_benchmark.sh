#!/bin/bash
# Phase 5: ACAT-X Full Benchmark (All 14 Dimensions)
# Evaluates all core + candidate dimensions across multiple models

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Configuration
MODELS=("ollama/phi" "ollama/mistral" "ollama/llama2")
DIMENSIONS=(
  # Core dimensions (8)
  "consist" "truth" "sycophancy" "harm"
  "service" "autonomy" "value" "humility"
  # Candidate dimensions (6)
  "handoff" "calibration" "boundary" "transparency" "temporal" "drift"
)
SAMPLES_PER_TEST=3

# Colors
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

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_phase() {
    echo -e "${CYAN}→ $1${NC}"
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

# Run full benchmark
print_header "Phase 5: Full Benchmark (All 14 Dimensions)"

total=$((${#MODELS[@]} * ${#DIMENSIONS[@]}))
current=0
start_time=$(date +%s)

for model in "${MODELS[@]}"; do
    model_name=${model##*/}
    echo ""
    print_phase "Testing: $model_name"

    for dimension in "${DIMENSIONS[@]}"; do
        ((current++))
        echo -n "  [$current/$total] $dimension ... "

        if python3 lightweight_eval_v2.py "$dimension" "$model" "$SAMPLES_PER_TEST" > /dev/null 2>&1; then
            print_success "Done"
        else
            print_warning "Failed"
        fi
    done
done

# Timing
end_time=$(date +%s)
elapsed=$((end_time - start_time))
minutes=$((elapsed / 60))
seconds=$((elapsed % 60))

# Summary
print_header "Phase 5 Complete"

echo -e "${CYAN}Results Summary:${NC}"
echo "  Total tests: $total"
echo "  Models: ${#MODELS[@]} (phi, mistral, llama2)"
echo "  Dimensions: ${#DIMENSIONS[@]} (8 core + 6 candidate)"
echo "  Time elapsed: ${minutes}m ${seconds}s"
echo ""
echo -e "${CYAN}Results saved to:${NC} results/lightweight_*.json"
echo ""
echo -e "${CYAN}Generate analysis:${NC}"
echo "  python3 analyze_results.py"
echo ""
echo -e "${CYAN}View raw results:${NC}"
echo "  cat results/lightweight_*.json | jq '.stats'"
echo ""

print_success "Phase 5 benchmark complete!"
