#!/usr/bin/env python3
"""
Phase 8 Analysis: Generate publication-grade benchmark report from batch results
Consumes phase8_batch_summary.json and generates PHASE8_BENCHMARK_REPORT.md
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict

def load_batch_summary():
    """Load batch summary results"""
    summary_file = Path("results") / "phase8_batch_summary.json"
    if not summary_file.exists():
        print(f"❌ Summary file not found: {summary_file}")
        return None

    with open(summary_file, "r") as f:
        return json.load(f)

def analyze_results(summary):
    """Analyze batch results and compute statistics"""

    results = summary.get("results", [])
    successful = [r for r in results if r["status"] == "success"]

    # Group by dimension and model
    by_dimension = defaultdict(list)
    by_model = defaultdict(list)

    for r in successful:
        dim = r["dimension"]
        model = r["model"].replace("ollama/", "").replace("anthropic/", "")
        score = r.get("score", 0)

        by_dimension[dim].append(score)
        by_model[model].append(score)

    # Calculate statistics
    stats = {
        "by_dimension": {},
        "by_model": {},
        "overall": {},
    }

    # Dimension stats
    for dim in sorted(by_dimension.keys()):
        scores = by_dimension[dim]
        stats["by_dimension"][dim] = {
            "avg": sum(scores) / len(scores) if scores else 0,
            "min": min(scores) if scores else 0,
            "max": max(scores) if scores else 0,
            "count": len(scores),
        }

    # Model stats
    for model in sorted(by_model.keys()):
        scores = by_model[model]
        stats["by_model"][model] = {
            "avg": sum(scores) / len(scores) if scores else 0,
            "min": min(scores) if scores else 0,
            "max": max(scores) if scores else 0,
            "count": len(scores),
        }

    # Overall stats
    all_scores = [r["score"] for r in successful]
    if all_scores:
        stats["overall"] = {
            "avg": sum(all_scores) / len(all_scores),
            "min": min(all_scores),
            "max": max(all_scores),
            "count": len(all_scores),
        }

    return stats, by_dimension, by_model

def generate_report(summary, stats, by_dimension, by_model):
    """Generate markdown report"""

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total_evals = summary.get("total_evaluations", 0)
    successful = summary.get("successful", 0)
    errors = summary.get("errors", 0)

    report = f"""# Phase 8 Benchmark Report: ACAT-X Multi-Tier Model Evaluation

**Generated:** {timestamp}
**Status:** Phase 8 Multi-Model Evaluation (Batch)

---

## Executive Summary

Comprehensive evaluation of ACAT-X across {len(summary.get('models', []))} models and {len(summary.get('dimensions', []))} evaluation dimensions.

### Key Metrics

- **Evaluations Completed:** {successful}/{total_evals}
- **Success Rate:** {(successful/total_evals*100):.1f}% if total_evals > 0 else 0
- **Overall Average Score:** {stats['overall'].get('avg', 0):.3f}
- **Score Range:** {stats['overall'].get('min', 0):.3f} - {stats['overall'].get('max', 0):.3f}

---

## Results by Model

"""

    for model in sorted(by_model.keys()):
        model_stats = stats["by_model"][model]
        report += f"### {model}\n"
        report += f"- **Samples Evaluated:** {model_stats['count']}\n"
        report += f"- **Average Score:** {model_stats['avg']:.3f}\n"
        report += f"- **Range:** {model_stats['min']:.3f} - {model_stats['max']:.3f}\n\n"

    report += "---\n\n## Results by Dimension\n\n"
    report += "| Dimension | Avg Score | Min | Max | N |\n"
    report += "|-----------|-----------|-----|-----|---|\n"

    for dim in sorted(by_dimension.keys()):
        dim_stats = stats["by_dimension"][dim]
        report += f"| {dim} | {dim_stats['avg']:.3f} | {dim_stats['min']:.3f} | {dim_stats['max']:.3f} | {dim_stats['count']} |\n"

    report += f"""
---

## Evaluation Framework

### Dimensions Assessed (14 core)
1. **Autonomy** - Agent independence and decision-making
2. **Boundary** - Scope limitation and constraint adherence
3. **Calibration** - Confidence accuracy and self-assessment
4. **Consist** - Internal consistency across outputs
5. **Drift** - Temporal stability and state management
6. **Handoff** - Work transfer and context preservation
7. **Harm** - Safety and harm prevention
8. **Humility** - Appropriate uncertainty expression
9. **Service** - Customer/user orientation
10. **Sycophancy** - Resistance to manipulation
11. **Temporal** - Time-awareness and planning
12. **Transparency** - Decision explanation clarity
13. **Truth** - Factual accuracy
14. **Value** - Value alignment and ethics

### Models Evaluated
"""

    for model in summary.get("models", []):
        model_display = model.replace("ollama/", "").replace("anthropic/", "")
        report += f"- {model_display}\n"

    report += f"""
---

## Summary

**Total Evaluations:** {total_evals}
**Successful:** {successful} ({(successful/total_evals*100):.1f}%)
**Errors:** {errors}

**Phase 8 Status:** {"✅ COMPLETE" if errors == 0 else "⚠️ PARTIAL"}

---

*Generated by ACAT-X Phase 8 Batch Evaluation Pipeline*
*Report timestamp: {datetime.now().isoformat()}*
"""

    return report

def main():
    print("\n" + "="*70)
    print("Phase 8 Analysis: Generating Benchmark Report")
    print("="*70 + "\n")

    summary = load_batch_summary()
    if not summary:
        return 1

    print(f"✅ Loaded batch summary: {summary['total_evaluations']} evaluations")

    stats, by_dimension, by_model = analyze_results(summary)
    print(f"✅ Analyzed results: {stats['overall'].get('count', 0)} successful")

    report = generate_report(summary, stats, by_dimension, by_model)

    report_file = Path("PHASE8_BENCHMARK_REPORT.md")
    with open(report_file, "w") as f:
        f.write(report)

    print(f"✅ Report generated: {report_file}")
    print("\n" + "="*70)
    print("Phase 8 Analysis Complete")
    print("="*70 + "\n")

    return 0

if __name__ == "__main__":
    sys.exit(main())
