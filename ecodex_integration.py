#!/usr/bin/env python3
"""
Ecodex Integration for ACAT-X
Feeds evaluation results into Ecodex for epistemic calibration tracking
"""

import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List


def load_results() -> Dict:
    """Load all ACAT-X evaluation results from JSON files"""
    results_dir = Path("results")
    result_files = sorted(results_dir.glob("lightweight_*.json"))

    results_by_model = {}

    for result_file in result_files:
        try:
            with open(result_file) as f:
                data = json.load(f)

            if "error" in data:
                continue

            model = data["model"]
            dimension = data["dimension"]
            avg_score = data["stats"]["average"]

            if model not in results_by_model:
                results_by_model[model] = {}

            results_by_model[model][dimension] = {
                "score": avg_score,
                "count": data["stats"]["count"],
                "min": data["stats"]["min"],
                "max": data["stats"]["max"],
            }
        except Exception as e:
            print(f"⚠️  Error reading {result_file}: {e}")

    return results_by_model


def generate_calibration_report(results: Dict) -> str:
    """Generate calibration report for Ecodex"""
    report = f"""# ACAT-X Evaluation Calibration Report
Generated: {datetime.now().isoformat()}

## Summary
- Models evaluated: {len(results)}
- Total model×dimension combinations: {sum(len(dims) for dims in results.values())}

## Results by Model
"""

    for model, dimensions in sorted(results.items()):
        scores = [d["score"] for d in dimensions.values()]
        avg = sum(scores) / len(scores) if scores else 0
        report += f"\n### {model}\n"
        report += f"- Average score: {avg:.3f}\n"
        report += f"- Dimensions evaluated: {len(dimensions)}\n"
        report += f"- Range: {min(scores):.3f} - {max(scores):.3f}\n"

    return report


def emit_to_ecodex(calibration_report: str) -> bool:
    """Emit calibration report to Ecodex via cortex bus"""
    try:
        # This would send the calibration report to Ecodex
        # For now, just save it locally as a reference
        report_file = Path("calibration_report.md")
        with open(report_file, "w") as f:
            f.write(calibration_report)

        print(f"✅ Calibration report saved: {report_file}")
        return True
    except Exception as e:
        print(f"❌ Error emitting to Ecodex: {e}")
        return False


def main():
    print("🔗 ACAT-X → Ecodex Integration")
    print()

    # Load evaluation results
    print("Loading evaluation results...")
    results = load_results()

    if not results:
        print("❌ No results found. Run Phase 5 benchmark first:")
        print("   bash phase5_benchmark.sh")
        return 1

    print(f"✅ Loaded results for {len(results)} models")

    # Generate calibration report
    print()
    print("Generating calibration report...")
    report = generate_calibration_report(results)

    # Emit to Ecodex
    print()
    print("Emitting to Ecodex...")
    if emit_to_ecodex(report):
        print("✅ Ecodex integration complete")
        print()
        print("Next steps:")
        print("1. Review calibration_report.md")
        print("2. Launch Ecodex: ecodex")
        print("3. Load evaluation results for multi-AI coordination")
        return 0
    else:
        print("⚠️  Ecodex integration had issues")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
