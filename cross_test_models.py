#!/usr/bin/env python3
"""
ACAT-X Cross-Model Evaluation
Test the same dimensions across multiple models and generate comparison reports
"""

import sys
import subprocess
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Models to test
MODELS = {
    "mistral": {
        "name": "Mistral 7B",
        "model": "ollama/mistral",
        "speed": "Medium",
        "quality": "Good",
        "reasoning": "Better",
    },
    "llama2": {
        "name": "Llama 2 7B",
        "model": "ollama/llama2:7b",
        "speed": "Slow",
        "quality": "Good",
        "reasoning": "Good",
    },
    "neural-chat": {
        "name": "Neural Chat",
        "model": "ollama/neural-chat",
        "speed": "Fast",
        "quality": "Fair",
        "reasoning": "Fair",
    },
    "phi": {
        "name": "Phi 2.7B",
        "model": "ollama/phi",
        "speed": "Very Fast",
        "quality": "Fair",
        "reasoning": "Good",
    },
    "claude": {
        "name": "Claude Opus 4.1 (API)",
        "model": "anthropic/claude-opus-4-1",
        "speed": "Fast",
        "quality": "Excellent",
        "reasoning": "Excellent",
        "requires_api": True,
    },
    "gpt4": {
        "name": "GPT-4 (API)",
        "model": "openai/gpt-4",
        "speed": "Fast",
        "quality": "Excellent",
        "reasoning": "Excellent",
        "requires_api": True,
    },
}

# Dimensions to test
DIMENSIONS = [
    "consist",
    "truth",
    "sycophancy",
    "harm",
    "service",
    "autonomy",
    "value",
    "humility",
]

def print_header(text):
    """Print a formatted header"""
    print(f"\n{'='*80}")
    print(f"  {text}")
    print(f"{'='*80}\n")

def check_model_available(model_key):
    """Check if model is available"""
    model_info = MODELS[model_key]

    if model_info.get("requires_api"):
        if model_key == "claude":
            return bool(os.environ.get("ANTHROPIC_API_KEY"))
        elif model_key == "gpt4":
            return bool(os.environ.get("OPENAI_API_KEY"))
    else:
        # Check if Ollama model is available
        model_name = model_info["model"].split("/")[-1]
        result = subprocess.run(
            ["ollama", "ls"],
            capture_output=True,
            text=True
        )
        return model_name in result.stdout

def run_evaluation(dimension, model_key):
    """Run a single evaluation"""
    model_info = MODELS[model_key]
    model = model_info["model"]

    print(f"  ▶ {dimension:15} with {model_info['name']:25} ", end="", flush=True)

    result_dir = f"results/{dimension}_{model_key}"

    try:
        result = subprocess.run(
            [
                "uv", "run", "python", "run_evaluation.py",
                dimension, model
            ],
            capture_output=True,
            text=True,
            timeout=300,  # 5 minute timeout per evaluation
        )

        if result.returncode == 0:
            print("✅")
            return True
        else:
            print(f"❌ Error")
            if result.stderr:
                print(f"     {result.stderr[:100]}")
            return False

    except subprocess.TimeoutExpired:
        print("❌ Timeout")
        return False
    except Exception as e:
        print(f"❌ {str(e)[:50]}")
        return False

def print_model_info():
    """Print available models and their characteristics"""
    print_header("Available Models")
    print(f"{'Model':<20} {'Speed':<12} {'Quality':<12} {'Reasoning':<12}")
    print("-" * 60)

    for key, info in MODELS.items():
        print(f"{info['name']:<20} {info['speed']:<12} {info['quality']:<12} {info['reasoning']:<12}")

    print("\nLocal models (Ollama):")
    print("  - mistral, llama2, neural-chat, phi")
    print("  Pull with: ollama pull <model>")
    print("\nAPI models (require environment variables):")
    print("  - claude (ANTHROPIC_API_KEY)")
    print("  - gpt4 (OPENAI_API_KEY)")

def run_cross_test(selected_models=None, selected_dimensions=None):
    """Run cross-model evaluation"""
    import os

    if selected_models is None:
        # Default: local models
        selected_models = ["mistral", "llama2"]

    if selected_dimensions is None:
        selected_dimensions = DIMENSIONS[:4]  # First 4 by default

    print_header("ACAT-X Cross-Model Evaluation")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Models: {', '.join(selected_models)}")
    print(f"Dimensions: {', '.join(selected_dimensions)}")

    # Check available models
    print_header("Checking Model Availability")
    available = {}
    for model in selected_models:
        if model not in MODELS:
            print(f"  ❌ Unknown model: {model}")
            continue

        model_info = MODELS[model]
        if model_info.get("requires_api"):
            if model == "claude" and not os.environ.get("ANTHROPIC_API_KEY"):
                print(f"  ⚠️  {model_info['name']}: Missing ANTHROPIC_API_KEY")
                continue
            elif model == "gpt4" and not os.environ.get("OPENAI_API_KEY"):
                print(f"  ⚠️  {model_info['name']}: Missing OPENAI_API_KEY")
                continue

        print(f"  ✅ {model_info['name']}")
        available[model] = True

    if not available:
        print("\n❌ No models available. Install Ollama or set API keys.")
        sys.exit(1)

    # Run evaluations
    print_header("Running Evaluations")
    print(f"Total: {len(selected_dimensions)} dimensions × {len(available)} models\n")

    results = {}
    for i, dimension in enumerate(selected_dimensions, 1):
        print(f"[{i}/{len(selected_dimensions)}] {dimension.upper()}")
        results[dimension] = {}

        for model in available:
            success = run_evaluation(dimension, model)
            results[dimension][model] = success

    # Summary
    print_header("Summary")
    total = len(selected_dimensions) * len(available)
    passed = sum(1 for d in results.values() for m in d.values() if m)
    print(f"Total evaluations: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")

    # Per-model summary
    print("\nPer-model results:")
    for model in available:
        model_info = MODELS[model]
        passed_for_model = sum(1 for d in results.values() if d.get(model))
        print(f"  {model_info['name']:25} {passed_for_model}/{len(selected_dimensions)}")

    print("\n✅ Evaluations complete!")
    print(f"Results saved to: results/")
    print(f"View results with: python scripts/compare_evaluations.py")

def main():
    if len(sys.argv) < 2:
        print("ACAT-X Cross-Model Evaluation")
        print("=" * 80)
        print("\nUsage:")
        print("  python cross_test_models.py --info")
        print("  python cross_test_models.py --quick")
        print("  python cross_test_models.py --full")
        print("  python cross_test_models.py mistral llama2 --dims consist truth")
        print("\nOptions:")
        print("  --info      Show available models")
        print("  --quick     Test mistral + llama2 on 4 dimensions")
        print("  --full      Test all local models on all dimensions")
        print("  --dims      Specify dimensions (comma-separated)")
        sys.exit(1)

    if sys.argv[1] == "--info":
        print_model_info()
    elif sys.argv[1] == "--quick":
        run_cross_test(
            selected_models=["mistral", "llama2"],
            selected_dimensions=DIMENSIONS[:4]
        )
    elif sys.argv[1] == "--full":
        run_cross_test(
            selected_models=["mistral", "llama2", "neural-chat"],
            selected_dimensions=DIMENSIONS
        )
    else:
        # Custom selection
        models = []
        dims = None

        for arg in sys.argv[1:]:
            if arg == "--dims":
                idx = sys.argv.index(arg)
                dims = sys.argv[idx + 1].split(",")
                break
            elif arg in MODELS:
                models.append(arg)

        if not models:
            models = ["mistral"]
        if not dims:
            dims = DIMENSIONS[:4]

        run_cross_test(selected_models=models, selected_dimensions=dims)

if __name__ == "__main__":
    main()
