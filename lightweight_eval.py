#!/usr/bin/env python3
"""
Lightweight ACAT-X Evaluator
Directly calls Ollama/Claude without Inspect AI overhead
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


def call_ollama(model_name: str, prompt: str) -> str:
    """Call Ollama model directly via CLI"""
    try:
        result = subprocess.run(
            ["ollama", "run", model_name],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=300,  # 5 minutes timeout for slow models
        )
        if result.returncode != 0:
            raise RuntimeError(f"Ollama error: {result.stderr}")
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        raise RuntimeError("Ollama request timed out (model too slow?)")
    except FileNotFoundError:
        raise RuntimeError("Ollama not found in PATH")


def get_model_output(model_spec: str, prompt: str) -> str:
    """Get model output for a prompt"""
    if model_spec.startswith("ollama/"):
        model_name = model_spec.replace("ollama/", "")
        return call_ollama(model_name, prompt)
    elif model_spec.startswith("anthropic/"):
        # Fall back to OpenAI client for Claude
        from openai import OpenAI
        client = OpenAI()
        response = client.messages.create(
            model=model_spec.replace("anthropic/", ""),
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        return response.content[0].text
    else:
        raise ValueError(f"Unknown model spec: {model_spec}")


def evaluate_dimension(
    dimension: str,
    model_spec: str,
    num_samples: int = 5,
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

    # Get samples from task
    try:
        samples = list(task.dataset)[:num_samples]
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
            model_output = get_model_output(model_spec, sample.input)
            elapsed = time.time() - start

            # Score the response
            score_result = None
            for scorer in task.scorers:
                try:
                    # Call scorer on the sample with the model output
                    score_result = scorer.score(
                        sample=sample,
                        state={},
                        model_output=model_output,
                    )
                except Exception as scorer_error:
                    print(f"\n  Scorer error: {scorer_error}")
                    continue

                if score_result:
                    break

            score_value = score_result.get("score", {}).get("value", 0) if score_result else 0
            scores.append(score_value)

            result = {
                "sample_id": i,
                "input": sample.input[:100],  # Truncate for readability
                "output": model_output[:200],
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
        print("Usage: python lightweight_eval.py <dimension> <model_spec> [num_samples]")
        print("\nExamples:")
        print("  python lightweight_eval.py consist ollama/phi")
        print("  python lightweight_eval.py consist ollama/phi 10")
        print("  python lightweight_eval.py truth ollama/mistral 5")
        sys.exit(1)

    dimension = sys.argv[1]
    model_spec = sys.argv[2]
    num_samples = int(sys.argv[3]) if len(sys.argv) > 3 else 5

    # Run evaluation
    result = evaluate_dimension(dimension, model_spec, num_samples)

    # Save results
    if "error" not in result or len(result.get("samples", [])) > 0:
        result_file = Path(f"results/lightweight_{dimension}_{model_spec.replace('/', '_')}.json")
        result_file.parent.mkdir(parents=True, exist_ok=True)

        with open(result_file, "w") as f:
            json.dump(result, f, indent=2)

        print(f"✅ Results saved to: {result_file}")
    else:
        print(f"❌ Evaluation failed: {result.get('error')}")
        sys.exit(1)


if __name__ == "__main__":
    main()
