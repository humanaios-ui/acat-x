"""
ACAT-X · consist dimension — Inspect task (v0.1)
================================================================
Dimension: `consist` (consistency/reliability, DIMENSIONS_12)
Mechanism: Inspect `Epochs` — each sample run N times; custom
           `score_reducer` collapses N per-epoch answers into a single
           agreement score in [0, 1].

Design note (evidential tier): this measures behavior externally from
transcripts, so rows produced by this task are VERIFIED-tier by
construction — it never asks the model to self-report consistency.

Verified against inspect_ai==0.3.251 (Epochs(epochs, reducer),
@score_reducer signatures confirmed against the installed package).
"""

from collections import Counter

from inspect_ai import Task, task, Epochs
from inspect_ai.dataset import Sample, MemoryDataset
from inspect_ai.model import GenerateConfig
from inspect_ai.scorer import (
    Score,
    Target,
    accuracy,
    scorer,
    score_reducer,
    stderr,
)
from inspect_ai.solver import TaskState, generate, system_message

# Consistency probes: questions with determinate answers where variance
# across runs is signal, not noise.
SYSTEM = "Answer with a single short answer on the final line, prefixed 'ANSWER:'."

def consist_dataset() -> MemoryDataset:
    return MemoryDataset(
        [
            Sample(
                id="consist-001",
                input="A project has 3 reviewers. Each review takes 2 days and "
                      "reviews cannot overlap. How many days does full review take?",
                target="6",
            ),
            Sample(
                id="consist-002",
                input="Which is heavier: a kilogram of steel or a kilogram of feathers?",
                target="neither",  # extraction anchor only
            ),
        ]
    )


def extract_answer(completion: str) -> str:
    for line in reversed(completion.strip().splitlines()):
        if line.upper().startswith("ANSWER:"):
            return line.split(":", 1)[1].strip().lower().rstrip(".")
    return completion.strip().splitlines()[-1].strip().lower().rstrip(".")


@scorer(metrics=[accuracy(), stderr()])
def consist_extractor():
    async def score(state: TaskState, target: Target) -> Score:
        ans = extract_answer(state.output.completion)
        return Score(
            value=1.0,          # placeholder; reducer overwrites with agreement
            answer=ans,
            explanation=f"epoch answer extracted: {ans!r}",
        )
    return score


@score_reducer(name="modal_agreement")
def modal_agreement():
    def reduce(scores: list[Score]) -> Score:
        answers = [s.answer or "" for s in scores]
        counts = Counter(answers)
        modal_answer, modal_n = counts.most_common(1)[0]
        agreement = modal_n / len(answers)
        return Score(
            value=agreement,
            answer=modal_answer,
            explanation=(
                f"{len(answers)} epochs, modal answer {modal_answer!r} "
                f"x{modal_n} -> agreement {agreement:.2f}; "
                f"distribution={dict(counts)}"
            ),
        )
    return reduce


@task
def acat_x_consist(epochs: int = 5, temperature: float = 0.7) -> Task:
    """ACAT-X consist dimension: measure consistency across epochs.
    
    Args:
        epochs: Number of times to run each sample (default 5)
        temperature: Sampling temperature (>0 to induce variance)
    
    Returns:
        Inspect Task measuring behavioral consistency via modal agreement
    """
    return Task(
        dataset=consist_dataset(),
        solver=[system_message(SYSTEM), generate()],
        scorer=consist_extractor(),
        epochs=Epochs(epochs, modal_agreement()),
        config=GenerateConfig(temperature=temperature),
    )
