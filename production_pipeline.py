#!/usr/bin/env python3
"""
Phase 6.4: Production Deployment Pipeline
Automated re-evaluation, result persistence, monitoring, and regression alerting.
"""

import json
import sqlite3
import subprocess
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# Configuration
PRODUCTION_DB = Path(".empirica/production_results.db")
RESULTS_ARCHIVE = Path("archive/production_runs")
ALERTS_LOG = Path("logs/regression_alerts.log")
MODELS_DEFAULT = ["ollama/phi", "ollama/llama2"]
DIMENSIONS_DEFAULT = ["autonomy", "boundary", "calibration", "consist", "drift", "handoff", "harm", "humility", "service", "sycophancy", "temporal", "transparency", "truth", "value"]


class ProductionDatabase:
    """SQLite storage for production evaluation results"""

    def __init__(self, db_path: Path = PRODUCTION_DB):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()

    def _init_schema(self):
        """Initialize database schema"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS evaluation_cycles (
                    cycle_id TEXT PRIMARY KEY,
                    start_time TEXT,
                    end_time TEXT,
                    status TEXT,
                    models_count INTEGER,
                    dimensions_count INTEGER,
                    results_count INTEGER
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS evaluation_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cycle_id TEXT,
                    model TEXT,
                    dimension TEXT,
                    score REAL,
                    samples INTEGER,
                    timestamp TEXT,
                    FOREIGN KEY (cycle_id) REFERENCES evaluation_cycles(cycle_id)
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS performance_alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cycle_id TEXT,
                    model TEXT,
                    dimension TEXT,
                    alert_type TEXT,
                    previous_score REAL,
                    current_score REAL,
                    change_pct REAL,
                    timestamp TEXT,
                    FOREIGN KEY (cycle_id) REFERENCES evaluation_cycles(cycle_id)
                )
            """)

            conn.commit()

    def record_cycle(self, cycle_id: str, start_time: str, status: str = "in_progress"):
        """Record cycle start"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO evaluation_cycles
                (cycle_id, start_time, status, models_count, dimensions_count, results_count)
                VALUES (?, ?, ?, 0, 0, 0)
            """, (cycle_id, start_time, status))
            conn.commit()

    def set_cycle_counts(self, cycle_id: str, models_count: int, dimensions_count: int):
        """Persist model/dimension counts for cycle telemetry."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                UPDATE evaluation_cycles
                SET models_count = ?, dimensions_count = ?
                WHERE cycle_id = ?
            """, (models_count, dimensions_count, cycle_id))
            conn.commit()

    def record_result(
        self,
        cycle_id: str,
        model: str,
        dimension: str,
        score: float,
        samples: int
    ):
        """Record individual evaluation result"""
        timestamp = datetime.now().isoformat()
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO evaluation_results
                (cycle_id, model, dimension, score, samples, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (cycle_id, model, dimension, score, samples, timestamp))
            conn.commit()

    def get_baseline(self, model: str, dimension: str, num_recent: int = 3) -> Optional[float]:
        """Get baseline score (average of recent runs)"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT score FROM evaluation_results
                WHERE model = ? AND dimension = ?
                ORDER BY timestamp DESC
                LIMIT ?
            """, (model, dimension, num_recent))
            scores = [row[0] for row in cursor.fetchall()]
            return sum(scores) / len(scores) if scores else None

    def record_alert(
        self,
        cycle_id: str,
        model: str,
        dimension: str,
        alert_type: str,
        prev_score: float,
        curr_score: float
    ):
        """Record performance regression alert"""
        change_pct = ((curr_score - prev_score) / max(prev_score, 0.01)) * 100
        timestamp = datetime.now().isoformat()

        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO performance_alerts
                (cycle_id, model, dimension, alert_type, previous_score, current_score, change_pct, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (cycle_id, model, dimension, alert_type, prev_score, curr_score, change_pct, timestamp))
            conn.commit()

    def finalize_cycle(self, cycle_id: str, status: str, results_count: int):
        """Mark cycle as complete"""
        end_time = datetime.now().isoformat()
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                UPDATE evaluation_cycles
                SET end_time = ?, status = ?, results_count = ?
                WHERE cycle_id = ?
            """, (end_time, status, results_count, cycle_id))
            conn.commit()


class ProductionPipeline:
    """Full production evaluation pipeline"""

    def __init__(self, models: List[str] = None, dimensions: List[str] = None, num_samples: int = 3):
        self.models = models or MODELS_DEFAULT
        self.dimensions = dimensions or DIMENSIONS_DEFAULT
        self.num_samples = num_samples
        self.db = ProductionDatabase()
        self.cycle_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.alerts = []
        self.results = []

    def run(self, dry_run: bool = False) -> Dict:
        """Execute full production evaluation cycle"""
        print(f"\n{'='*60}")
        print(f"Production Evaluation Cycle: {self.cycle_id}")
        print(f"{'='*60}")
        print(f"Models: {len(self.models)} | Dimensions: {len(self.dimensions)}")
        print(f"Expected evaluations: {len(self.models) * len(self.dimensions)}")

        start_time = datetime.now().isoformat()
        self.db.record_cycle(self.cycle_id, start_time)
        self.db.set_cycle_counts(self.cycle_id, len(self.models), len(self.dimensions))

        if dry_run:
            print("(DRY RUN - not executing)")
            self.db.finalize_cycle(self.cycle_id, "dry_run", 0)
            return {"status": "dry_run", "cycle_id": self.cycle_id, "results_count": 0, "alerts": 0, "report": "Dry run - no evaluation executed"}

        results_count = 0

        for model_idx, model in enumerate(self.models, 1):
            for dim_idx, dimension in enumerate(self.dimensions, 1):
                progress = f"[{model_idx}/{len(self.models)}][{dim_idx}/{len(self.dimensions)}]"
                print(f"{progress} {model} / {dimension} ... ", end="", flush=True)

                try:
                    # Run evaluation
                    result = self._run_evaluation(model, dimension, self.num_samples)

                    if result:
                        score = result.get("stats", {}).get("average", 0.0)
                        samples = result.get("stats", {}).get("count", 0)

                        # Record result
                        self.db.record_result(self.cycle_id, model, dimension, score, samples)

                        # Check for regression
                        self._check_regression(model, dimension, score)

                        self.results.append({
                            "model": model,
                            "dimension": dimension,
                            "score": score,
                            "samples": samples
                        })

                        print(f"✅ {score:.3f}")
                        results_count += 1
                    else:
                        print(f"⚠️  No results")

                except Exception as e:
                    print(f"❌ Error: {str(e)[:40]}")

        # Finalize cycle
        status = "completed" if results_count > 0 else "failed"
        self.db.finalize_cycle(self.cycle_id, status, results_count)

        # Archive results
        self._archive_results()

        # Generate report
        report = self._generate_report(results_count)

        return {
            "status": status,
            "cycle_id": self.cycle_id,
            "results_count": results_count,
            "alerts": len(self.alerts),
            "report": report
        }

    def _run_evaluation(self, model: str, dimension: str, num_samples: int = 3) -> Optional[Dict]:
        """Run single evaluation"""
        model_safe = model.replace("/", "_")
        result_file = Path("results") / f"lightweight_{dimension}_{model_safe}.json"

        try:
            cmd = [
                sys.executable,
                "lightweight_eval.py",
                dimension,
                model,
                str(num_samples),
                "--seed",
                "42",
                "--retries",
                "2",
                "--timeout",
                "90",
            ]
            subprocess.run(cmd, capture_output=True, timeout=600, check=False)

            # Load result
            if result_file.exists():
                with open(result_file, "r") as f:
                    return json.load(f)
        except subprocess.TimeoutExpired:
            print("timeout")
        except Exception as e:
            print(f"error: {e}")

        return None

    def _check_regression(self, model: str, dimension: str, current_score: float):
        """Detect performance regression"""
        baseline = self.db.get_baseline(model, dimension, num_recent=3)

        if baseline is not None:
            regression_threshold = 0.15  # 15% drop is significant
            change = (baseline - current_score) / max(baseline, 0.01)

            if change > regression_threshold:
                alert = {
                    "model": model,
                    "dimension": dimension,
                    "baseline": baseline,
                    "current": current_score,
                    "regression_pct": change * 100
                }
                self.alerts.append(alert)
                self.db.record_alert(
                    self.cycle_id, model, dimension, "regression",
                    baseline, current_score
                )
                self._write_alert_log(alert)
                print(f"\n⚠️  REGRESSION ALERT: {model}/{dimension} {baseline:.3f} → {current_score:.3f}")

    def _write_alert_log(self, alert: Dict) -> None:
        """Append alert to persistent log and optional webhook sink."""
        ALERTS_LOG.parent.mkdir(parents=True, exist_ok=True)
        line = (
            f"{datetime.now().isoformat()} cycle={self.cycle_id} model={alert['model']} "
            f"dimension={alert['dimension']} baseline={alert['baseline']:.3f} "
            f"current={alert['current']:.3f} regression_pct={alert['regression_pct']:.2f}\n"
        )
        with open(ALERTS_LOG, "a", encoding="utf-8") as f:
            f.write(line)

    def _archive_results(self):
        """Archive cycle results"""
        archive_dir = RESULTS_ARCHIVE / self.cycle_id
        archive_dir.mkdir(parents=True, exist_ok=True)

        for result_file in Path("results").glob("lightweight_*.json"):
            dest = archive_dir / result_file.name
            result_file.rename(dest)

    def _generate_report(self, results_count: int) -> str:
        """Generate summary report"""
        report = f"""
Production Cycle Report: {self.cycle_id}
{'='*60}
Status: Completed
Results: {results_count} evaluations
Alerts: {len(self.alerts)} regressions detected
Timestamp: {datetime.now().isoformat()}

Model Performance Summary:
"""
        model_scores = {}
        for result in self.results:
            model = result["model"]
            score = result["score"]
            if model not in model_scores:
                model_scores[model] = []
            model_scores[model].append(score)

        for model, scores in sorted(model_scores.items()):
            avg = sum(scores) / len(scores) if scores else 0
            report += f"  {model}: {avg:.3f} avg ({len(scores)} dims)\n"

        if self.alerts:
            report += f"\nRegressions Detected:\n"
            for alert in self.alerts:
                report += f"  - {alert['model']}/{alert['dimension']}: {alert['regression_pct']:.1f}% drop\n"

        return report


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Production evaluation pipeline")
    parser.add_argument("--dry-run", action="store_true", help="Dry run (no execution)")
    parser.add_argument("--models", nargs="+", default=MODELS_DEFAULT, help="Models to evaluate")
    parser.add_argument("--dimensions", nargs="+", default=DIMENSIONS_DEFAULT, help="Dimensions to evaluate")
    parser.add_argument("--samples", type=int, default=3, help="Samples per evaluation (default: 3)")
    parser.add_argument("--report", action="store_true", help="Show performance report")

    args = parser.parse_args()

    pipeline = ProductionPipeline(args.models, args.dimensions, args.samples)

    if args.report:
        # Show historical trends
        db = ProductionDatabase()
        print("Production Evaluation History (last 5 cycles)")
        print("(Future: integrate with dashboard)")
    else:
        result = pipeline.run(dry_run=args.dry_run)
        print(f"\n{'='*60}")
        print(f"Cycle Summary:")
        print(f"  Status: {result['status']}")
        print(f"  Results: {result['results_count']}")
        print(f"  Alerts: {result['alerts']}")
        print(f"{'='*60}")
