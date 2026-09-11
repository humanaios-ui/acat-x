from __future__ import annotations

from pathlib import Path

from lightweight_eval import parse_args
from monitoring_dashboard import ProductionMonitor
from production_pipeline import ProductionDatabase


def test_parse_args_sets_seed_and_defaults() -> None:
    cfg = parse_args(["truth", "ollama/mock"])
    assert cfg.seed == 42
    assert cfg.retries == 2
    assert cfg.timeout_seconds == 60


def test_monitor_health_check(tmp_path: Path) -> None:
    db_path = tmp_path / "prod.db"
    db = ProductionDatabase(db_path)
    db.record_cycle("cycle-1", "2026-01-01T00:00:00", "in_progress")
    db.set_cycle_counts("cycle-1", 1, 14)
    db.finalize_cycle("cycle-1", "completed", 14)

    monitor = ProductionMonitor(db_path)
    health = monitor.health_check()
    assert health["ok"] is True
    assert health["latest_cycle"] == "cycle-1"
