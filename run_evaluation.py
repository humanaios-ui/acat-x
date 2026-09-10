#!/usr/bin/env python3
"""
ACAT-X Evaluation Runner
Runs Inspect AI evaluations with proper task discovery
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from inspect_ai import eval as inspect_eval

from acat_x.autonomy import acat_x_autonomy
from acat_x.boundary import acat_x_boundary
from acat_x.calibration import acat_x_calibration
from acat_x.consist import acat_x_consist
from acat_x.drift import acat_x_drift
from acat_x.handoff import acat_x_handoff
from acat_x.harm import acat_x_harm
from acat_x.humility import acat_x_humility
from acat_x.service import acat_x_service
from acat_x.sycophancy import acat_x_sycophancy
from acat_x.temporal import acat_x_temporal
from acat_x.transparency import acat_x_transparency
from acat_x.truth import acat_x_truth
from acat_x.value import acat_x_value

# Task registry
TASKS = {
    "consist": acat_x_consist,
    "truth": acat_x_truth,
    "sycophancy": acat_x_sycophancy,
    "harm": acat_x_harm,
    "service": acat_x_service,
    "autonomy": acat_x_autonomy,
    "value": acat_x_value,
    "humility": acat_x_humility,
    "handoff": acat_x_handoff,
    "calibration": acat_x_calibration,
    "boundary": acat_x_boundary,
    "transparency": acat_x_transparency,
    "temporal": acat_x_temporal,
    "drift": acat_x_drift,
}

def main():
    if len(sys.argv) < 3:
        print("Usage: python run_evaluation.py <task_name> <model>")
        print(f"\nAvailable tasks: {', '.join(TASKS.keys())}")
        print("\nExample:")
        print("  python run_evaluation.py consist ollama/mistral")
        print("  python run_evaluation.py truth anthropic/claude-opus-4-1")
        sys.exit(1)

    task_name = sys.argv[1]
    model = sys.argv[2]

    if task_name not in TASKS:
        print(f"❌ Unknown task: {task_name}")
        print(f"Available: {', '.join(TASKS.keys())}")
        sys.exit(1)

    print("🚀 Running ACAT-X evaluation")
    print(f"   Task: {task_name}")
    print(f"   Model: {model}")
    print()

    task_fn = TASKS[task_name]
    task = task_fn()

    # Run evaluation (synchronous call)
    inspect_eval(
        task,
        model=model,
        log_dir=f"results/{task_name}_{model.replace('/', '_')}",
    )

    print("\n✅ Evaluation complete!")
    print(f"   Results saved to: results/{task_name}_{model.replace('/', '_')}")

if __name__ == "__main__":
    main()
