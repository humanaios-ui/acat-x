#!/usr/bin/env python3
"""
Phase 7 Analysis: Deep dive into Phi 14-dimension baseline
Generates comparison reports and publication materials
"""

import json
import sqlite3
from collections import defaultdict
from datetime import datetime
from pathlib import Path

DB_PATH = Path(".empirica/production_results.db")

def get_cycle_results(cycle_id):
    """Query all results for a cycle"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("""
            SELECT model, dimension, score, samples, timestamp
            FROM evaluation_results
            WHERE cycle_id = ?
            ORDER BY model, dimension
        """, (cycle_id,))
        return cursor.fetchall()

def analyze_phi_baseline(cycle_id):
    """Analyze Phi results across all dimensions"""
    results = get_cycle_results(cycle_id)

    if not results:
        return {"error": "No results found", "cycle_id": cycle_id}

    # Group by dimension
    dim_scores = defaultdict(list)
    for model, dimension, score, samples, ts in results:
        if model == "ollama/phi":
            dim_scores[dimension].append(score)

    # Calculate statistics
    stats = {}
    for dim, scores in sorted(dim_scores.items()):
        if scores:
            stats[dim] = {
                "score": scores[0],  # Single sample
                "samples": len(scores),
                "avg": sum(scores) / len(scores)
            }

    # Overall performance
    all_scores = [v["score"] for v in stats.values()]
    overall = {
        "average": sum(all_scores) / len(all_scores) if all_scores else 0,
        "min": min(all_scores) if all_scores else 0,
        "max": max(all_scores) if all_scores else 0,
        "dimensions_tested": len(stats),
        "total_samples": len(all_scores),
    }

    return {
        "cycle_id": cycle_id,
        "model": "ollama/phi",
        "overall": overall,
        "dimensions": stats,
        "timestamp": datetime.now().isoformat()
    }

def generate_report(analysis):
    """Generate markdown report"""
    if "error" in analysis:
        return f"Error: {analysis['error']}"

    report = f"""# Phase 7 Baseline Analysis: Phi 14-Dimension Evaluation

**Cycle ID:** {analysis['cycle_id']}
**Model:** Phi (1.6 GB, 3B parameters)
**Evaluated:** {datetime.now().isoformat()}

## Overall Performance

| Metric | Value |
|--------|-------|
| Average Score | {analysis['overall']['average']:.3f} |
| Min Score | {analysis['overall']['min']:.3f} |
| Max Score | {analysis['overall']['max']:.3f} |
| Dimensions Tested | {analysis['overall']['dimensions_tested']} |
| Total Samples | {analysis['overall']['total_samples']} |

## Dimension Results

| Dimension | Score | Status |
|-----------|-------|--------|
"""

    for dim, stats in sorted(analysis['dimensions'].items()):
        score = stats['score']
        status = "✅ Good" if score > 0.6 else "⚠️  Needs work" if score > 0.3 else "❌ Poor"
        report += f"| {dim:15} | {score:.3f} | {status} |\n"

    report += """

## Interpretation

- **High performers (>0.7):** These dimensions show strong baseline capability
- **Medium (0.3-0.7):** Dimensions with room for improvement
- **Low (<0.3):** Dimensions needing semantic scoring or task refinement

## Next Steps

1. Compare with Phase 5 partial baseline (6 dimensions)
2. Analyze why certain dimensions underperform
3. Semantic scoring integration for improved discrimination
4. Publication manuscript draft

---

*Analysis complete. Ready for Phase 7 publication deliverables.*
"""

    return report

if __name__ == "__main__":
    import sys
    cycle_id = sys.argv[1] if len(sys.argv) > 1 else None

    if not cycle_id:
        print("Usage: python3 phase7_analysis.py <cycle_id>")
        sys.exit(1)

    analysis = analyze_phi_baseline(cycle_id)

    # Save JSON
    with open(f"results/phase7_analysis_{cycle_id}.json", "w") as f:
        json.dump(analysis, f, indent=2)

    # Generate and save report
    report = generate_report(analysis)
    with open(f"docs/PHASE7_REPORT_{cycle_id}.md", "w") as f:
        f.write(report)

    print(report)
    print(f"\n✅ Analysis saved to results/phase7_analysis_{cycle_id}.json")
    print(f"✅ Report saved to docs/PHASE7_REPORT_{cycle_id}.md")
