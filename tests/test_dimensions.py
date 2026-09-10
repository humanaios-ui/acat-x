from __future__ import annotations

import importlib

import pytest
from inspect_ai import Task

DIMENSIONS = [
    "consist",
    "truth",
    "sycophancy",
    "harm",
    "service",
    "autonomy",
    "value",
    "humility",
    "handoff",
    "calibration",
    "boundary",
    "transparency",
    "temporal",
    "drift",
]


@pytest.mark.parametrize("dimension", DIMENSIONS)
def test_dimension_task_loads_with_dataset(dimension: str) -> None:
    module = importlib.import_module(f"acat_x.{dimension}")
    factory = getattr(module, f"acat_x_{dimension}")

    task = factory()

    assert isinstance(task, Task)
    samples = list(task.dataset)
    assert len(samples) >= 2
    assert all(getattr(sample, "input", None) for sample in samples)
