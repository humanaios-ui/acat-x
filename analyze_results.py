#!/usr/bin/env python3
"""Analyze ACAT-X evaluation results and generate comparison report"""

import json
from collections import defaultdict
from pathlib import Path


def analyze_results():
    """Analyze all lightweight evaluation results"""
    results_dir = Path("results")
    result_files = sorted(results_dir.glob("lightweight_*.json"))

    if not result_files:
        print("❌ No results found. Run evaluations first:")
        print("  bash ./fast_benchmark.sh")
        return None

    print("\n" + "="*80)
    print("ACAT-X Lightweight Evaluation Results".center(80))
    print("="*80 + "\n")

    # Collect results by model and dimension
    results_by_model_dim = {}
    all_models = set()
    all_dimensions = set()

    for result_file in result_files:
        try:
            with open(result_file) as f:
                data = json.load(f)

            if "error" in data:
                print(f"⚠️  {result_file.name}: {data['error']}")
                continue

            model = data["model"]
            dimension = data["dimension"]
            avg_score = data["stats"]["average"]

            all_models.add(model)
            all_dimensions.add(dimension)
            results_by_model_dim[(model, dimension)] = {
                "average": avg_score,
                "min": data["stats"]["min"],
                "max": data["stats"]["max"],
                "count": data["stats"]["count"],
            }

        except Exception as e:
            print(f"⚠️  Error reading {result_file}: {e}")
            continue

    if not results_by_model_dim:
        print("❌ No valid results found")
        return None

    # Display results table
    models = sorted(all_models)
    dimensions = sorted(all_dimensions)

    print("Summary by Model & Dimension (Average Score):")
    print("-" * 80)

    # Header
    header = "Dimension".ljust(15)
    for model in models:
        header += f" | {model.ljust(12)}"
    print(header)
    print("-" * 80)

    # Rows
    dim_averages = defaultdict(list)
    for dim in dimensions:
        row = dim.ljust(15)
        for model in models:
            score = results_by_model_dim.get((model, dim), {}).get("average", 0)
            dim_averages[dim].append(score)
            row += f" | {score:8.3f}"
        print(row)

    print("-" * 80)

    # Calculate and display model averages
    print("\nModel Performance Summary:")
    print("-" * 80)
    model_averages = {}
    for model in models:
        scores = [
            results_by_model_dim.get((model, dim), {}).get("average", 0)
            for dim in dimensions
        ]
        avg = sum(scores) / len(scores) if scores else 0
        model_averages[model] = avg
        min_score = min(scores) if scores else 0
        max_score = max(scores) if scores else 0
        print(f"{model.ljust(15)}: {avg:6.3f} (range: {min_score:.3f} - {max_score:.3f})")

    print("\nDimension Performance Summary:")
    print("-" * 80)
    for dim in dimensions:
        scores = dim_averages[dim]
        avg = sum(scores) / len(scores) if scores else 0
        min_score = min(scores) if scores else 0
        max_score = max(scores) if scores else 0
        print(f"{dim.ljust(15)}: {avg:6.3f} (range: {min_score:.3f} - {max_score:.3f})")

    # Best performers
    print("\n" + "="*80)
    print("Best Performers:")
    print("-" * 80)
    best_model = max(model_averages.items(), key=lambda x: x[1])
    print(f"  Model: {best_model[0]} ({best_model[1]:.3f})")

    best_dim_scores = [(d, sum(dim_averages[d])/len(dim_averages[d])) for d in dimensions]
    best_dim = max(best_dim_scores, key=lambda x: x[1])
    print(f"  Dimension: {best_dim[0]} ({best_dim[1]:.3f})")

    print("\n" + "="*80)
    print(f"✅ Analysis complete! Evaluated {len(results_by_model_dim)} model × dimension combinations")
    print("="*80 + "\n")

    return results_by_model_dim

if __name__ == "__main__":
    analyze_results()
