#!/usr/bin/env python3
"""
ACAT-X Evaluator v3: Ollama + Claude + GPT-4 support
Extended lightweight_eval_v2.py with API model support
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent / "src"))


def call_ollama(model_name: str, prompt: str) -> str:
    """Call Ollama model via CLI"""
    try:
        result = subprocess.run(
            ["ollama", "run", model_name],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=60,
        )
        if result.returncode != 0:
            raise RuntimeError(f"Ollama error: {result.stderr}")
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        raise RuntimeError("Ollama request timed out")


def call_claude(model_name: str, prompt: str) -> str:
    """Call Claude via Anthropic API"""
    try:
        from anthropic import Anthropic
        client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        message = client.messages.create(
            model=model_name,
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}],
        )
        return message.content[0].text
    except ImportError:
        raise RuntimeError("anthropic package required: pip install anthropic")
    except Exception as e:
        raise RuntimeError(f"Claude API error: {e}")


def call_gpt4(model_name: str, prompt: str) -> str:
    """Call GPT-4 via OpenAI API"""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model=model_name,
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content
    except ImportError:
        raise RuntimeError("openai package required: pip install openai")
    except Exception as e:
        raise RuntimeError(f"OpenAI API error: {e}")


def get_model_output(model_spec: str, prompt: str) -> str:
    """Get output from any model: Ollama, Claude, or GPT-4"""
    if model_spec.startswith("ollama/"):
        model_name = model_spec.replace("ollama/", "")
        return call_ollama(model_name, prompt)
    elif model_spec.startswith("anthropic/"):
        model_name = model_spec.replace("anthropic/", "")
        return call_claude(model_name, prompt)
    elif model_spec.startswith("openai/"):
        model_name = model_spec.replace("openai/", "")
        return call_gpt4(model_name, prompt)
    else:
        raise ValueError(f"Unknown model spec: {model_spec}")


def simple_score(model_output: str, target: str) -> float:
    """Simple scoring for Phase 5 compatibility"""
    if not target or not model_output:
        return 0.5
    output_lower = model_output.lower()
    target_lower = target.lower()
    if target_lower in output_lower or target_lower == output_lower:
        return 1.0
    words = target_lower.split()
    if words and words[0] in output_lower:
        return 0.7
    return 0.2


def evaluate_dimension(dimension: str, model_spec: str, num_samples: int = 3) -> dict:
    """Evaluate a dimension across any model type"""
    model_name = model_spec.replace("ollama/", "").replace("anthropic/", "").replace("openai/", "")

    print(f"\n{'='*60}")
    print(f"Dimension: {dimension.upper()}")
    print(f"Model: {model_name}")
    print(f"Samples: {num_samples}")
    print(f"{'='*60}\n")

    try:
        task_module = __import__(f"acat_x.{dimension}", fromlist=[f"acat_x_{dimension}"])
        task_fn = getattr(task_module, f"acat_x_{dimension}")
        task = task_fn()
    except Exception as e:
        print(f"❌ Failed to load task {dimension}: {e}")
        return {"error": str(e), "dimension": dimension, "model": model_name}

    try:
        samples = list(task.dataset)[:num_samples]
        if not samples:
            return {"error": "No samples", "dimension": dimension, "model": model_name}
    except Exception as e:
        return {"error": str(e), "dimension": dimension, "model": model_name}

    results = []
    scores = []

    for i, sample in enumerate(samples, 1):
        try:
            print(f"[{i}/{num_samples}] ", end="", flush=True)
            start = time.time()
            model_output = get_model_output(model_spec, sample.input)
            elapsed = time.time() - start

            target = getattr(sample, 'target', '')
            score_value = simple_score(model_output, target)
            scores.append(score_value)

            result = {
                "sample_id": i,
                "input": sample.input[:100],
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

    if scores:
        avg_score = sum(scores) / len(scores)
        min_score = min(scores)
        max_score = max(scores)
    else:
        avg_score = min_score = max_score = 0

    print(f"\n{'─'*60}")
    print(f"Summary: {len(results)} samples, {avg_score:.3f} avg")
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
        print("Usage: python lightweight_eval_v3_apis.py <dimension> <model_spec> [num_samples]")
        print("\nModel specs:")
        print("  ollama/phi, ollama/mistral, ollama/llama2")
        print("  anthropic/claude-opus, anthropic/claude-sonnet")
        print("  openai/gpt-4, openai/gpt-4-turbo")
        sys.exit(1)

    dimension = sys.argv[1]
    model_spec = sys.argv[2]
    num_samples = int(sys.argv[3]) if len(sys.argv) > 3 else 3

    result = evaluate_dimension(dimension, model_spec, num_samples)

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
