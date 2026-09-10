from __future__ import annotations

from run_evaluation import TASKS


def test_task_registry_has_14_dimensions() -> None:
    assert len(TASKS) == 14


def test_task_registry_entries_callable() -> None:
    for name, fn in TASKS.items():
        task = fn()
        assert task is not None, f"Task factory failed for {name}"
