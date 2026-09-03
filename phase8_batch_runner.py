#!/usr/bin/env python3
"""
Phase 8 Batch Evaluation Runner
Executes lightweight_eval_v3_apis.py for all model/dimension combinations
Aggregates results from JSON output files
"""

import subprocess
import json
import sys
from pathlib import Path
from datetime import datetime

MODELS = [
    "ollama/phi",
    "ollama/mistral",
    "ollama/llama2",
    "anthropic/claude-haiku-4.5-20250101",
]

DIMENSIONS = [
    "autonomy", "boundary", "calibration", "consist",
    "drift", "handoff", "harm", "humility",
    "service", "sycophancy", "temporal", "transparency",
    "truth", "value"
]

SAMPLES_PER_DIM = 1


def run_evaluation(dimension, model, num_samples=SAMPLES_PER_DIM):
    """Run single evaluation and return result dict"""
    try:
        result = subprocess.run(
            ["python3", "lightweight_eval_v3_apis.py", dimension, model, str(num_samples)],
            capture_output=True,
            text=True,
            timeout=180,
        )

        if result.returncode != 0:
            return {
                "status": "error",
                "dimension": dimension,
                "model": model,
                "error": result.stderr[:200] if result.stderr else "Non-zero exit",
            }

        # Parse JSON from result file
        model_safe = model.replace("/", "_")
        result_file = Path("results") / f"lightweight_{dimension}_{model_safe}.json"

        if result_file.exists():
            with open(result_file, "r") as f:
                data = json.load(f)
            return {
                "status": "success",
                "dimension": dimension,
                "model": model,
                "score": data.get("stats", {}).get("average", 0),
                "samples": data.get("stats", {}).get("count", 0),
            }
        else:
            return {
                "status": "error",
                "dimension": dimension,
                "model": model,
                "error": f"Result file not created: {result_file}",
            }

    except subprocess.TimeoutExpired:
        return {
            "status": "timeout",
            "dimension": dimension,
            "model": model,
            "error": "Evaluation exceeded 180s timeout",
        }
    except Exception as e:
        return {
            "status": "error",
            "dimension": dimension,
            "model": model,
            "error": str(e)[:100],
        }


def main():
    print(f"\n{'='*70}")
    print(f"Phase 8 Batch Evaluation Runner")
    print(f"Models: {len(MODELS)} | Dimensions: {len(DIMENSIONS)} | Samples/Dim: {SAMPLES_PER_DIM}")
    print(f"Total evaluations: {len(MODELS) * len(DIMENSIONS)}")
    print(f"{'='*70}\n")

    results = []
    success_count = 0
    error_count = 0

    for model_idx, model in enumerate(MODELS, 1):
        print(f"\n[Model {model_idx}/{len(MODELS)}] {model}")
        print(f"{'─'*70}")

        for dim_idx, dimension in enumerate(DIMENSIONS, 1):
            print(f"  [{dim_idx:2d}/{len(DIMENSIONS)}] {dimension:12s} ... ", end="", flush=True)

            result = run_evaluation(dimension, model, SAMPLES_PER_DIM)
            results.append(result)

            if result["status"] == "success":
                score = result.get("score", 0)
                print(f"✅ Score: {score:.3f}")
                success_count += 1
            else:
                error = result.get("error", "Unknown error")
                print(f"❌ {error[:40]}")
                error_count += 1

    # Summary
    print(f"\n{'='*70}")
    print(f"Batch Results: {success_count}/{len(results)} successful, {error_count} errors")
    print(f"{'='*70}\n")

    # Group by dimension for summary
    dim_summary = {}
    for r in results:
        dim = r["dimension"]
        if dim not in dim_summary:
            dim_summary[dim] = []
        dim_summary[dim].append(r)

    print("\nResults by Dimension:")
    for dim in DIMENSIONS:
        if dim in dim_summary:
            dim_results = dim_summary[dim]
            successful = [r for r in dim_results if r["status"] == "success"]
            if successful:
                scores = [r["score"] for r in successful]
                avg = sum(scores) / len(scores)
                print(f"  {dim:12s}: {len(successful)}/{len(dim_results)} models | avg: {avg:.3f}")
            else:
                print(f"  {dim:12s}: 0/{len(dim_results)} models | all failed")

    # Save aggregate results
    summary = {
        "timestamp": datetime.now().isoformat(),
        "total_evaluations": len(results),
        "successful": success_count,
        "errors": error_count,
        "results": results,
        "dimensions": DIMENSIONS,
        "models": MODELS,
    }

    summary_file = Path("results") / "phase8_batch_summary.json"
    with open(summary_file, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\n✅ Summary saved to: {summary_file}")

    return 0 if error_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
