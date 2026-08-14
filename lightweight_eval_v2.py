#!/usr/bin/env python3
"""
Lightweight ACAT-X Evaluator v2
Directly calls Ollama without Inspect AI overhead — simpler scoring
"""

import sys
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Tuple

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))


def call_ollama(model_name: str, prompt: str, temperature: float = 0.7) -> str:
    """Call Ollama model directly via CLI"""
    try:
        result = subprocess.run(
            ["ollama", "run", model_name],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=60,  # 60 second timeout per call
        )
        if result.returncode != 0:
            raise RuntimeError(f"Ollama error: {result.stderr}")
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        raise RuntimeError("Ollama request timed out")
    except FileNotFoundError:
        raise RuntimeError("Ollama not found in PATH")


def simple_score(model_output: str, target: str) -> float:
    """Simple scoring: check if output contains or matches target"""
    if not target or not model_output:
        return 0.5  # neutral

    # Normalize for comparison
    output_lower = model_output.lower()
    target_lower = target.lower()

    # Exact match or contains
    if target_lower in output_lower or target_lower == output_lower:
        return 1.0

    # Partial match (first word or significant substring)
    words = target_lower.split()
    if words and words[0] in output_lower:
        return 0.7

    # No match
    return 0.2


def evaluate_dimension(
    dimension: str,
    model_spec: str,
    num_samples: int = 3,
) -> dict:
    """Run evaluation for a single dimension"""

    model_name = model_spec.replace("ollama/", "").replace("anthropic/", "")

    print(f"\n{'='*60}")
    print(f"Dimension: {dimension.upper()}")
    print(f"Model: {model_name}")
    print(f"Samples: {num_samples}")
    print(f"{'='*60}\n")

    # Load the task module dynamically
    try:
        task_module = __import__(f"acat_x.{dimension}", fromlist=[f"acat_x_{dimension}"])
        task_fn = getattr(task_module, f"acat_x_{dimension}")
        task = task_fn()
    except Exception as e:
        print(f"❌ Failed to load task {dimension}: {e}")
        return {"error": str(e), "dimension": dimension, "model": model_name}

    # Get samples from task dataset
    try:
        samples = list(task.dataset)[:num_samples]
        if not samples:
            print(f"❌ No samples found in dataset")
            return {"error": "No samples", "dimension": dimension, "model": model_name}
    except Exception as e:
        print(f"❌ Failed to get samples: {e}")
        return {"error": str(e), "dimension": dimension, "model": model_name}

    results = []
    scores = []

    for i, sample in enumerate(samples, 1):
        try:
            print(f"[{i}/{num_samples}] ", end="", flush=True)

            # Generate model response
            start = time.time()
            model_output = call_ollama(model_name, sample.input)
            elapsed = time.time() - start

            # Simple scoring
            target = getattr(sample, 'target', '')
            score_value = simple_score(model_output, target)
            scores.append(score_value)

            result = {
                "sample_id": i,
                "input": sample.input[:100],  # Truncate for readability
                "output": model_output[:200],
                "target": target[:100] if target else "",
                "score": score_value,
                "elapsed_sec": elapsed,
            }
            results.append(result)

            print(f"✅ Score: {score_value:.3f} ({elapsed:.1f}s)")

        except Exception as e:
            print(f"⚠️  Sample error: {e}")
            continue

    # Compute statistics
    if scores:
        avg_score = sum(scores) / len(scores)
        min_score = min(scores)
        max_score = max(scores)
    else:
        avg_score = min_score = max_score = 0

    # Summary
    print(f"\n{'─'*60}")
    print(f"Summary:")
    print(f"  Samples completed: {len(results)}")
    print(f"  Average score: {avg_score:.3f}")
    print(f"  Range: {min_score:.3f} - {max_score:.3f}")
    print(f"{'─'*60}\n")

    return {
        "dimension": dimension,
        "model": model_name,
        "samples": results,
        "stats": {
            "count": len(results),
            "average": avg_score,
            "min": min_score,
            "max": max_score,
        },
        "timestamp": datetime.now().isoformat(),
    }


def main():
    if len(sys.argv) < 3:
        print("Usage: python lightweight_eval_v2.py <dimension> <model_spec> [num_samples]")
        print("\nExamples:")
        print("  python lightweight_eval_v2.py consist ollama/phi")
        print("  python lightweight_eval_v2.py consist ollama/phi 3")
        print("  python lightweight_eval_v2.py truth ollama/mistral 5")
        sys.exit(1)

    dimension = sys.argv[1]
    model_spec = sys.argv[2]
    num_samples = int(sys.argv[3]) if len(sys.argv) > 3 else 3

    # Run evaluation
    result = evaluate_dimension(dimension, model_spec, num_samples)

    # Save to results directory
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)

    model_safe = model_spec.replace("/", "_")
    result_file = results_dir / f"lightweight_{dimension}_{model_safe}.json"

    with open(result_file, "w") as f:
        json.dump(result, f, indent=2)

    if "error" not in result:
        print(f"✅ Results saved to: {result_file}")
    else:
        print(f"⚠️  Results (with errors) saved to: {result_file}")

    return 0 if "error" not in result else 1


if __name__ == "__main__":
    sys.exit(main())
