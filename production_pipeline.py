#!/usr/bin/env python3
"""Phase 6.4: Production Deployment Pipeline"""

import json
import subprocess
from pathlib import Path
from datetime import datetime


def run_evaluation_cycle(models, dimensions):
    """Full production evaluation cycle"""
    results = []
    for model in models:
        for dim in dimensions:
            cmd = f"python3 lightweight_eval_v3_apis.py {dim} {model} 3"
            subprocess.run(cmd, shell=True)
            result_file = f"results/lightweight_{dim}_{model.replace('/', '_')}.json"
            if Path(result_file).exists():
                results.append(result_file)
    return results


def archive_results(cycle_date):
    """Archive results to storage"""
    archive_dir = Path(f"archive/{cycle_date}")
    archive_dir.mkdir(parents=True, exist_ok=True)
    for f in Path("results").glob("*.json"):
        f.rename(archive_dir / f.name)


def generate_report(cycle_date):
    """Generate comparison report"""
    import subprocess
    subprocess.run("python3 analyze_results.py > reports/report_{}.txt".format(cycle_date), shell=True)


if __name__ == "__main__":
    cycle = datetime.now().strftime("%Y%m%d_%H%M%S")
    models = ["ollama/phi", "ollama/mistral", "anthropic/claude-opus", "openai/gpt-4"]
    dims = ["consist", "truth", "sycophancy", "harm"]

    print(f"Starting production cycle: {cycle}")
    results = run_evaluation_cycle(models, dims)
    archive_results(cycle)
    generate_report(cycle)
    print(f"✅ Cycle complete. Results: {len(results)} tests")
