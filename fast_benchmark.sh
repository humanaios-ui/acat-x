#!/bin/bash
# Fast ACAT-X Benchmark using lightweight evaluator (no Inspect AI overhead)

set -euo pipefail

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"
source "$SCRIPT_DIR/scripts/common.sh"

# Configuration
MODELS=("ollama/phi" "ollama/mistral")
DIMENSIONS=("consist" "truth" "sycophancy" "harm")
SAMPLES_PER_TEST=3

print_header "Checking Ollama"
check_ollama

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

        if python3 lightweight_eval.py "$dimension" "$model" "$SAMPLES_PER_TEST" > /dev/null 2>&1; then
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
