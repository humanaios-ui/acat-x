#!/usr/bin/env python3
"""View evaluation results in a nice format"""

import json
from pathlib import Path

from tabulate import tabulate


def view_results():
    """Display all lightweight evaluation results"""
    results_dir = Path("results")
    result_files = list(results_dir.glob("lightweight_*.json"))

    if not result_files:
        print("❌ No results found yet. Run evaluations first:")
        print("  python lightweight_eval.py consist ollama/phi")
        return

    print("\n" + "="*70)
    print("ACAT-X Evaluation Results".center(70))
    print("="*70 + "\n")

    # Collect all results by model and dimension
    results_by_model = {}

    for result_file in sorted(result_files):
        with open(result_file) as f:
            data = json.load(f)

        if "error" in data:
            continue

        model = data["model"]
        dimension = data["dimension"]

        if model not in results_by_model:
            results_by_model[model] = {}

        results_by_model[model][dimension] = data["stats"]["average"]

    # Display results
    if not results_by_model:
        print("❌ No valid results found")
        return

    # Summary table
    dimensions = sorted(set(d for m in results_by_model.values() for d in m.keys()))
    models = sorted(results_by_model.keys())

    table_data = []
    for model in models:
        row = [model]
        for dim in dimensions:
            score = results_by_model[model].get(dim, "N/A")
            if isinstance(score, float):
                row.append(f"{score:.3f}")
            else:
                row.append(score)
        table_data.append(row)

    print(tabulate(table_data, headers=["Model"] + dimensions, tablefmt="grid"))

    # Detailed view
    print("\n" + "="*70)
    print("Detailed Results".center(70))
    print("="*70 + "\n")

    for result_file in sorted(result_files):
        with open(result_file) as f:
            data = json.load(f)

        if "error" in data:
            print(f"❌ {result_file.name}: {data['error']}")
            continue

        print(f"📊 {data['model'].upper()} / {data['dimension'].upper()}")
        print(f"   Samples: {data['stats']['count']}")
        print(f"   Average: {data['stats']['average']:.3f}")
        print(f"   Range: {data['stats']['min']:.3f} - {data['stats']['max']:.3f}")
        print()

    print("="*70)

if __name__ == "__main__":
    view_results()
