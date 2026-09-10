#!/bin/bash
# ACAT-X Multi-Model Evaluation Script
# Usage: ./scripts/evaluate_multiple_models.sh [dimensions] [--quick]

set -euo pipefail

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( dirname "$SCRIPT_DIR" )"
source "$SCRIPT_DIR/common.sh"

# Default dimensions (can override with arguments)
DIMENSIONS="${1:-consist truth sycophancy harm service autonomy value humility}"
QUICK_MODE="${2:-}"

# Results directory
RESULTS_DIR="$PROJECT_ROOT/results"
mkdir -p "$RESULTS_DIR"

# Models to test
MODELS=(
    "ollama/llama2:7b:Llama 2 7B (Local)"
    "ollama/mistral:Mistral 7B (Local)"
    "anthropic/claude-opus-4-1:Claude Opus (API)"
)

echo "=========================================="
echo "ACAT-X Multi-Model Evaluation"
echo "=========================================="
echo "Dimensions: $DIMENSIONS"
echo "Models: ${#MODELS[@]}"
echo "Quick mode: ${QUICK_MODE:-off}"
echo ""

# Check if uv is available
if ! command -v uv &> /dev/null; then
    echo "ERROR: 'uv' not found. Install from https://docs.astral.sh/uv/getting-started/"
    exit 1
fi

# Function to run evaluation for one model
evaluate_model() {
    local model_spec="$1"
    local display_name="$2"
    local model_id=$(echo "$model_spec" | tr '/' '_' | tr ':' '_')

    echo ""
    echo "=========================================="
    echo "Testing: $display_name"
    echo "Model: $model_spec"
    echo "=========================================="

    # Check if model is available (for ollama)
    if [[ "$model_spec" == ollama* ]]; then
        model_name=$(echo "$model_spec" | cut -d/ -f2)
        if ! ollama ls | grep -q "$model_name"; then
            echo "WARNING: $model_name not found in Ollama"
            echo "Install with: ollama pull $model_name"
            echo "Skipping..."
            return
        fi
    fi

    # Build eval command safely as array
    local eval_cmd=(uv run inspect eval-set)
    for dim in $DIMENSIONS; do
        eval_cmd+=("src/acat_x/$dim")
    done
    eval_cmd+=(--model "$model_spec" --log-dir "$RESULTS_DIR/$model_id")

    # Add quick mode limits
    if [[ -n "$QUICK_MODE" ]] && [[ "$QUICK_MODE" == "--quick" ]]; then
        eval_cmd+=(--max-samples 1)
    fi

    echo "Command: ${eval_cmd[*]}"
    echo ""

    # Run evaluation
    cd "$PROJECT_ROOT"
    if "${eval_cmd[@]}"; then
        echo "✅ $display_name completed successfully"
        echo "Results: $RESULTS_DIR/$model_id"
    else
        echo "❌ $display_name failed"
    fi
}

# Run evaluations
echo "Starting evaluations at $(date)"

for model_info in "${MODELS[@]}"; do
    IFS=':' read -r model_spec display_name <<< "$model_info"
    evaluate_model "$model_spec" "$display_name"
done

# Summary
echo ""
echo "=========================================="
echo "Evaluation Complete"
echo "=========================================="
echo "Results saved in: $RESULTS_DIR"
echo ""
echo "To compare results:"
echo "  python3 scripts/compare_evaluations.py"
echo ""
echo "To view results for a specific model:"
echo "  uv run inspect info $RESULTS_DIR/ollama_llama2_7b"
