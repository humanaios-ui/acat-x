#!/usr/bin/env python3
"""
Compare ACAT-X evaluation results across multiple models.
Analyzes scores, consistency, and ranking across dimensions.
"""

import json
import sys
from pathlib import Path
from collections import defaultdict
from statistics import mean, stdev

def load_results(results_dir):
    """Load all evaluation results from results directory."""
    results = {}
    results_path = Path(results_dir)

    if not results_path.exists():
        print(f"ERROR: Results directory not found: {results_dir}")
        sys.exit(1)

    # Iterate through model directories
    for model_dir in sorted(results_path.iterdir()):
        if not model_dir.is_dir():
            continue

        model_name = model_dir.name
        model_results = {}

        # Iterate through dimensions
        for dim_dir in sorted(model_dir.iterdir()):
            if not dim_dir.is_dir():
                continue

            dim_name = dim_dir.name
            results_file = dim_dir / "results.json"

            if results_file.exists():
                try:
                    with open(results_file) as f:
                        data = json.load(f)
                        scores = [r.get('score', {}).get('value', 0)
                                 for r in data.get('results', [])]
                        if scores:
                            model_results[dim_name] = {
                                'scores': scores,
                                'mean': mean(scores),
                                'count': len(scores),
                                'stdev': stdev(scores) if len(scores) > 1 else 0,
                            }
                except Exception as e:
                    print(f"ERROR parsing {results_file}: {e}")

        if model_results:
            results[model_name] = model_results

    return results

def print_summary(results):
    """Print evaluation summary comparison."""
    if not results:
        print("No results found to compare.")
        return

    print("\n" + "=" * 100)
    print("ACAT-X EVALUATION COMPARISON")
    print("=" * 100)

    # Get all dimensions
    all_dims = set()
    for model_results in results.values():
        all_dims.update(model_results.keys())
    all_dims = sorted(all_dims)

    # Print overall scores by model
    print("\n1. OVERALL SCORES BY MODEL (Average across all dimensions)")
    print("-" * 100)
    print(f"{'Model':<35} {'Mean Score':<15} {'Std Dev':<15} {'Dimensions':<15}")
    print("-" * 100)

    model_summaries = []
    for model_name in sorted(results.keys()):
        model_results = results[model_name]
        means = [r['mean'] for r in model_results.values()]
        overall_mean = mean(means) if means else 0
        overall_stdev = mean([r['stdev'] for r in model_results.values()]) if means else 0

        model_summaries.append({
            'name': model_name,
            'mean': overall_mean,
            'stdev': overall_stdev,
            'count': len(model_results)
        })

        print(f"{model_name:<35} {overall_mean:>6.3f}           {overall_stdev:>6.3f}           {len(model_results):<15}")

    # Print per-dimension comparison
    print("\n2. SCORES BY DIMENSION")
    print("-" * 100)

    for dim in all_dims:
        print(f"\n{dim.upper()}")
        print("  " + "-" * 96)
        print(f"  {'Model':<30} {'Mean':<10} {'Std Dev':<10} {'Samples':<10}")
        print("  " + "-" * 96)

        dim_scores = []
        for model_name in sorted(results.keys()):
            if dim in results[model_name]:
                result = results[model_name][dim]
                dim_scores.append({
                    'model': model_name,
                    'mean': result['mean'],
                    'stdev': result['stdev'],
                    'count': result['count']
                })
                print(f"  {model_name:<30} {result['mean']:>6.3f}    {result['stdev']:>6.3f}    {result['count']:<10}")

        # Best performer for this dimension
        if dim_scores:
            best = max(dim_scores, key=lambda x: x['mean'])
            print(f"  ✓ Best: {best['model']} ({best['mean']:.3f})")

    # Print ranking
    print("\n3. MODEL RANKING (by overall score)")
    print("-" * 100)

    sorted_models = sorted(model_summaries, key=lambda x: x['mean'], reverse=True)
    for rank, model in enumerate(sorted_models, 1):
        ranking_bar = "█" * int(model['mean'] * 50) + "░" * (50 - int(model['mean'] * 50))
        print(f"{rank}. {model['name']:<30} {model['mean']:>6.3f}  {ranking_bar}")

    # Print consistency
    print("\n4. CONSISTENCY (lower is better)")
    print("-" * 100)
    print(f"{'Model':<35} {'Avg Std Dev':<20}")
    print("-" * 100)

    for model in sorted_models:
        print(f"{model['name']:<35} {model['stdev']:>6.3f}")

    print("\n" + "=" * 100)

def main():
    results_dir = Path(__file__).parent.parent / "results"

    if len(sys.argv) > 1:
        results_dir = Path(sys.argv[1])

    results = load_results(str(results_dir))
    print_summary(results)

if __name__ == "__main__":
    main()
