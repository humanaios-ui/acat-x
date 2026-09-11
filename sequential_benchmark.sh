#!/bin/bash
# ACAT-X Sequential Model Benchmark
# Tests each model on the same dimensions for fair comparison
# Run this after pulling all desired models with `ollama pull <model>`

set -euo pipefail

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"
source "$SCRIPT_DIR/scripts/common.sh"

# Configuration
MODELS=("mistral" "phi" "llama2:7b")
DIMENSIONS=("consist" "truth" "sycophancy" "harm")
BENCHMARK_DIR="results/benchmark_$(date +%Y%m%d_%H%M%S)"

check_model_available() {
    local model=$1
    local model_name=${model%%:*}  # Remove version suffix

    result=$(curl -s http://localhost:11434/api/tags)
    if echo "$result" | grep -q "$model_name"; then
        return 0
    else
        return 1
    fi
}

run_evaluation() {
    local dimension=$1
    local model=$2
    local model_display=$3

    echo -n "  ▶ ${dimension:15} with ${model_display:25} ... "

    if uv run python lightweight_eval.py "$dimension" "ollama/$model" 3 > /dev/null 2>&1; then
        print_success "Done"
        return 0
    else
        print_warning "Failed"
        return 1
    fi
}

main() {
    print_header "ACAT-X Sequential Model Benchmark"

    echo "Configuration:"
    echo "  Models: ${MODELS[@]}"
    echo "  Dimensions: ${DIMENSIONS[@]}"
    echo "  Results dir: $BENCHMARK_DIR"
    echo ""

    # Check Ollama
    check_ollama
    echo ""

    # Check available models
    print_header "Checking Model Availability"

    available_models=()
    for model in "${MODELS[@]}"; do
        if check_model_available "$model"; then
            print_success "$model available"
            available_models+=("$model")
        else
            print_warning "$model not found (pull with: ollama pull $model)"
        fi
    done

    if [ ${#available_models[@]} -eq 0 ]; then
        echo ""
        echo "❌ No models available. Pull at least one:"
        echo "  ollama pull mistral"
        echo "  ollama pull phi"
        echo "  ollama pull llama2:7b"
        exit 1
    fi

    echo ""
    echo "Will test: ${available_models[@]}"
    echo ""

    # Run benchmarks
    print_header "Running Benchmarks"

    total_tests=$((${#available_models[@]} * ${#DIMENSIONS[@]}))
    current_test=0
    passed=0
    failed=0

    for model in "${available_models[@]}"; do
        model_display=$(echo "$model" | sed 's/:.*$//')  # Get base name
        echo ""
        print_header "Testing: $model_display"

        for dimension in "${DIMENSIONS[@]}"; do
            ((current_test++))
            echo -n "[${current_test}/${total_tests}] "

            if run_evaluation "$dimension" "$model" "$model_display"; then
                ((passed++))
            else
                ((failed++))
            fi
        done
    done

    # Summary
    print_header "Benchmark Summary"

    echo "Total tests: $total_tests"
    echo "Passed: $passed"
    echo "Failed: $failed"
    echo ""

    if [ $failed -eq 0 ]; then
        print_success "All benchmarks passed!"
    else
        print_warning "$failed benchmark(s) failed"
    fi

    # Generate comparison report
    echo ""
    print_header "Generating Comparison Report"

    if python scripts/compare_evaluations.py > /tmp/benchmark_report.txt 2>&1; then
        print_success "Comparison report generated"
        echo ""
        head -50 /tmp/benchmark_report.txt
        echo ""
        echo "Full report available in terminal above"
    else
        print_warning "Could not generate comparison report"
    fi

    # Final summary
    print_header "Complete!"

    echo "Results saved in: results/"
    echo ""
    echo "To view results:"
    echo "  ls results/"
    echo "  python scripts/compare_evaluations.py"
    echo ""
    echo "To share results:"
    echo "  cat results/*/results.json | jq '.results[].score.value'"
    echo ""
}

# Run main
main
