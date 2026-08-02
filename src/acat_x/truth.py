"""ACAT-X · truth dimension — Factual accuracy evaluation (stub v0.1)"""

from inspect_ai import Task, task
from inspect_ai.dataset import MemoryDataset, Sample


def truth_dataset() -> MemoryDataset:
    """Stub: Load grounded truth questions + reference answers."""
    return MemoryDataset([
        Sample(id="truth-001", input="What is the capital of France?", target="Paris"),
    ])


@task
def acat_x_truth() -> Task:
    """ACAT-X truth dimension: measure factual accuracy.
    
    Implementation in progress: external fact-checking scorer.
    """
    raise NotImplementedError("Truth task implementation in progress")
