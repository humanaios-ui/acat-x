#!/usr/bin/env python3
"""
Phase 6.4 Monitoring: Dashboard and trend analysis
Reads from production database to generate monitoring reports.
"""

import sqlite3
import sys
from pathlib import Path
from typing import Dict, List, Tuple

PRODUCTION_DB = Path(".empirica/production_results.db")


class ProductionMonitor:
    """Query and analyze production evaluation data"""

    def __init__(self, db_path: Path = PRODUCTION_DB):
        self.db_path = db_path

    def get_latest_cycle(self) -> Tuple[str, Dict]:
        """Get latest evaluation cycle and stats"""
        if not self.db_path.exists():
            return None, {"error": "No production data yet"}

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT cycle_id, status, models_count, dimensions_count, results_count, start_time, end_time
                FROM evaluation_cycles
                ORDER BY start_time DESC
                LIMIT 1
            """)
            row = cursor.fetchone()
            if not row:
                return None, {"error": "No cycles found"}

            cycle_id, status, models, dims, results, start_time, end_time = row
            return cycle_id, {
                "status": status,
                "models": models,
                "dimensions": dims,
                "results": results,
                "start_time": start_time,
                "end_time": end_time
            }

    def get_model_scores(self, limit_cycles: int = 5) -> Dict[str, List]:
        """Get model performance trends"""
        if not self.db_path.exists():
            return {}

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT model, dimension, score, timestamp
                FROM evaluation_results
                ORDER BY timestamp DESC
                LIMIT ?
            """, (limit_cycles * 6 * 2,))  # Rough estimate: 6 dims × 2 models

            results = {}
            for model, dim, score, ts in cursor.fetchall():
                key = f"{model}/{dim}"
                if key not in results:
                    results[key] = []
                results[key].append((score, ts))

            return results

    def detect_regressions(self, threshold_pct: float = 15.0) -> List[Dict]:
        """Get recorded regression alerts"""
        if not self.db_path.exists():
            return []

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT model, dimension, alert_type, previous_score, current_score, change_pct, timestamp
                FROM performance_alerts
                ORDER BY timestamp DESC
                LIMIT 20
            """)

            alerts = []
            for model, dim, alert_type, prev, curr, change, ts in cursor.fetchall():
                alerts.append({
                    "model": model,
                    "dimension": dim,
                    "type": alert_type,
                    "previous": prev,
                    "current": curr,
                    "change_pct": change,
                    "timestamp": ts
                })

            return alerts

    def generate_report(self) -> str:
        """Generate monitoring report"""
        cycle_id, cycle_info = self.get_latest_cycle()

        if cycle_id is None:
            return "No production data available yet."

        report = f"""
╔════════════════════════════════════════════════════════════════╗
║           ACAT-X Phase 6 Production Monitor                   ║
╚════════════════════════════════════════════════════════════════╝

LATEST CYCLE: {cycle_id}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Status:       {cycle_info.get('status', 'unknown')}
Results:      {cycle_info.get('results', 0)} evaluations
Models:       {cycle_info.get('models', 0)}
Dimensions:   {cycle_info.get('dimensions', 0)}
Started:      {cycle_info.get('start_time', 'unknown')}
Completed:    {cycle_info.get('end_time', 'unknown')}

REGRESSIONS DETECTED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

        alerts = self.detect_regressions()
        if alerts:
            for alert in alerts[:5]:
                report += f"\n⚠️  {alert['model']}/{alert['dimension']}"
                report += f"\n   {alert['previous']:.3f} → {alert['current']:.3f} ({alert['change_pct']:+.1f}%)"
        else:
            report += "\n✅ No regressions detected\n"

        report += "\nMODEL PERFORMANCE SUMMARY\n"
        report += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"

        scores = self.get_model_scores(limit_cycles=1)
        if scores:
            # Group by model
            model_stats = {}
            for key, values in scores.items():
                model = key.split("/")[0]
                if model not in model_stats:
                    model_stats[model] = []
                if values:
                    model_stats[model].append(values[0][0])

            for model in sorted(model_stats.keys()):
                scores_list = model_stats[model]
                avg = sum(scores_list) / len(scores_list)
                report += f"\n{model}\n"
                report += f"  Average:  {avg:.3f}\n"
                report += f"  Samples:  {len(scores_list)}\n"
        else:
            report += "\nNo model performance data yet\n"

        report += "\n" + "="*65 + "\n"
        return report

    def health_check(self) -> Dict:
        """Basic operational health for monitoring integrations."""
        cycle_id, cycle_info = self.get_latest_cycle()
        alerts = self.detect_regressions()
        return {
            "ok": cycle_id is not None and "error" not in cycle_info,
            "latest_cycle": cycle_id,
            "status": cycle_info.get("status") if isinstance(cycle_info, dict) else None,
            "recent_alerts": len(alerts),
            "db_path": str(self.db_path),
        }

    def export_json(self) -> Dict:
        """Export monitoring data as JSON"""
        cycle_id, cycle_info = self.get_latest_cycle()
        return {
            "cycle": cycle_id,
            "cycle_info": cycle_info,
            "alerts": self.detect_regressions(),
            "scores": self.get_model_scores()
        }


if __name__ == "__main__":
    monitor = ProductionMonitor()

    if "--json" in sys.argv:
        import json
        print(json.dumps(monitor.export_json(), indent=2))
    elif "--health" in sys.argv:
        import json
        print(json.dumps(monitor.health_check(), indent=2))
    else:
        print(monitor.generate_report())
