#!/usr/bin/env python3
"""Canonical lightweight ACAT-X evaluator for local/API models."""

from __future__ import annotations

import argparse
import json
import os
import random
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

sys.path.insert(0, str(Path(__file__).parent / "src"))

from acat_x.errors import (  # noqa: E402
    ConfigurationError,
    DatasetError,
    ModelInvocationError,
    TaskLoadError,
)
from acat_x.scoring_utils import combined_score  # noqa: E402

DEFAULT_TIMEOUT_SECONDS = 60
DEFAULT_RETRIES = 2


@dataclass(frozen=True)
class RunConfig:
    dimension: str
    model_spec: str
    num_samples: int
    timeout_seconds: int
    retries: int
    semantic_weight: float
    seed: int


def _set_seed(seed: int) -> None:
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)


def _call_ollama(model_name: str, prompt: str, timeout_seconds: int) -> str:
    try:
        result = subprocess.run(
            ["ollama", "run", model_name],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise ModelInvocationError(f"Ollama request timed out after {timeout_seconds}s") from exc
    except FileNotFoundError as exc:
        raise ModelInvocationError("Ollama executable not found in PATH") from exc

    if result.returncode != 0:
        raise ModelInvocationError((result.stderr or "Ollama process failed").strip())

    return result.stdout.strip()


def _call_claude(model_name: str, prompt: str) -> str:
    try:
        from anthropic import Anthropic
    except ImportError as exc:
        raise ModelInvocationError("Missing dependency: anthropic") from exc

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ConfigurationError("ANTHROPIC_API_KEY is required for anthropic/* models")

    client = Anthropic(api_key=api_key)
    try:
        message = client.messages.create(
            model=model_name,
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}],
        )
    except Exception as exc:  # pragma: no cover - network/API failure path
        raise ModelInvocationError(f"Anthropic API error: {exc}") from exc

    first_block = message.content[0]
    return getattr(first_block, "text", str(first_block))


def _call_openai(model_name: str, prompt: str) -> str:
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise ModelInvocationError("Missing dependency: openai") from exc

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ConfigurationError("OPENAI_API_KEY is required for openai/* models")

    client = OpenAI(api_key=api_key)
    try:
        response = client.chat.completions.create(
            model=model_name,
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}],
        )
    except Exception as exc:  # pragma: no cover - network/API failure path
        raise ModelInvocationError(f"OpenAI API error: {exc}") from exc

    content = response.choices[0].message.content
    return content or ""


def get_model_output(model_spec: str, prompt: str, timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS) -> str:
    if model_spec.startswith("ollama/"):
        return _call_ollama(model_spec.replace("ollama/", "", 1), prompt, timeout_seconds)
    if model_spec.startswith("anthropic/"):
        return _call_claude(model_spec.replace("anthropic/", "", 1), prompt)
    if model_spec.startswith("openai/"):
        return _call_openai(model_spec.replace("openai/", "", 1), prompt)
    raise ConfigurationError(f"Unknown model spec: {model_spec}")


def _load_task(dimension: str):
    try:
        task_module = __import__(f"acat_x.{dimension}", fromlist=[f"acat_x_{dimension}"])
        task_fn = getattr(task_module, f"acat_x_{dimension}")
        return task_fn()
    except Exception as exc:
        raise TaskLoadError(f"Failed to load task '{dimension}': {exc}") from exc


def _extract_samples(task: Any, num_samples: int):
    try:
        samples = list(task.dataset)[:num_samples]
    except Exception as exc:
        raise DatasetError(f"Failed to extract samples: {exc}") from exc

    if not samples:
        raise DatasetError("Task dataset is empty")
    return samples


def evaluate_dimension(config: RunConfig) -> Dict[str, Any]:
    _set_seed(config.seed)

    task = _load_task(config.dimension)
    samples = _extract_samples(task, config.num_samples)

    results = []
    failures = []

    for i, sample in enumerate(samples, 1):
        target = str(getattr(sample, "target", "") or "")

        attempt_error: Optional[str] = None
        output = ""
        elapsed = 0.0

        for attempt in range(config.retries + 1):
            start = time.time()
            try:
                output = get_model_output(config.model_spec, sample.input, config.timeout_seconds)
                elapsed = time.time() - start
                attempt_error = None
                break
            except (ModelInvocationError, ConfigurationError) as exc:
                elapsed = time.time() - start
                attempt_error = str(exc)
                if attempt >= config.retries:
                    failures.append({
                        "sample_id": i,
                        "error": attempt_error,
                        "attempts": attempt + 1,
                    })

        if attempt_error and not output:
            continue

        breakdown = combined_score(output, target, semantic_weight=config.semantic_weight)

        results.append(
            {
                "sample_id": i,
                "input": sample.input[:200],
                "output": output[:400],
                "target": target[:200],
                "score": breakdown.combined,
                "score_breakdown": asdict(breakdown),
                "elapsed_sec": elapsed,
            }
        )

    scores = [r["score"] for r in results]

    return {
        "dimension": config.dimension,
        "model": config.model_spec,
        "stats": {
            "count": len(results),
            "average": (sum(scores) / len(scores)) if scores else 0.0,
            "min": min(scores) if scores else 0.0,
            "max": max(scores) if scores else 0.0,
            "failures": len(failures),
        },
        "samples": results,
        "failures": failures,
        "run_config": asdict(config),
        "timestamp": datetime.now().isoformat(),
    }


def parse_args(argv: list[str]) -> RunConfig:
    parser = argparse.ArgumentParser(description="Canonical lightweight ACAT-X evaluator")
    parser.add_argument("dimension", help="ACAT-X dimension module name")
    parser.add_argument("model_spec", help="Model spec, e.g. ollama/phi or anthropic/claude-opus-4-1")
    parser.add_argument("num_samples", nargs="?", type=int, default=3)
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_SECONDS)
    parser.add_argument("--retries", type=int, default=DEFAULT_RETRIES)
    parser.add_argument("--semantic-weight", type=float, default=0.3)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args(argv)

    if args.num_samples <= 0:
        raise ConfigurationError("num_samples must be > 0")
    if args.timeout <= 0:
        raise ConfigurationError("timeout must be > 0")

    return RunConfig(
        dimension=args.dimension,
        model_spec=args.model_spec,
        num_samples=args.num_samples,
        timeout_seconds=args.timeout,
        retries=max(0, args.retries),
        semantic_weight=max(0.0, min(1.0, args.semantic_weight)),
        seed=args.seed,
    )


def main(argv: Optional[list[str]] = None) -> int:
    try:
        config = parse_args(argv if argv is not None else sys.argv[1:])
        result = evaluate_dimension(config)
    except (ConfigurationError, TaskLoadError, DatasetError) as exc:
        print(f"❌ {exc}")
        return 1

    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)
    model_safe = config.model_spec.replace("/", "_")
    result_file = results_dir / f"lightweight_{config.dimension}_{model_safe}.json"

    with open(result_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    if result["stats"]["count"] == 0:
        print(f"⚠️  Evaluation completed with no successful samples: {result_file}")
        return 1

    print(f"✅ Results saved to: {result_file}")
    print(
        f"   count={result['stats']['count']} avg={result['stats']['average']:.3f} "
        f"failures={result['stats']['failures']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
