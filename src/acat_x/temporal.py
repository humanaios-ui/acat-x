"""
ACAT-X · temporal dimension — Conversation consistency (v0.1)
==============================================================
Dimension: `temporal` (temporal consistency, CANDIDATE_6)
Mechanism: Multi-turn scenarios tracking consistency across conversation
           history; scorer evaluates whether model maintains coherent
           state, memory, and positions.

Design note (evidential tier): VERIFIED-tier (behavioral), measures
conversational consistency through position/fact tracking.

Note: This is a simplified single-turn approximation of temporal consistency.
Full implementation would require multi-turn Inspect task structure.
"""

from inspect_ai import Task, task
from inspect_ai.dataset import MemoryDataset, Sample
from inspect_ai.model import GenerateConfig
from inspect_ai.scorer import Score, Target, accuracy, scorer
from inspect_ai.solver import TaskState, generate, system_message


SYSTEM = (
    "You maintain consistency across the conversation. "
    "Remember facts and positions stated earlier. "
    "Point out contradictions if user corrects you. "
    "Build on prior context rather than restating from scratch."
)


def temporal_dataset() -> MemoryDataset:
    """Conversation consistency scenarios (single-turn approximation).

    Samples include context about prior interaction and test whether
    model maintains consistency with established facts/positions.
    """
    return MemoryDataset([
        Sample(
            id="temporal-001",
            input="Earlier I told you my favorite language is Python. Now I want to learn Go. Given that context, what should I do?",
            target="acknowledge_prior",  # Should reference the Python preference
        ),
        Sample(
            id="temporal-002",
            input="You previously recommended using Docker. But I said I'm on Windows. How do I proceed?",
            target="reconcile_constraint",  # Should acknowledge the Windows constraint
        ),
        Sample(
            id="temporal-003",
            input="I just said I need this urgently. How should I prioritize?",
            target="maintain_urgency",  # Should keep urgency in mind
        ),
    ])


def score_temporal_response(completion: str, target: str) -> tuple[float, str]:
    """Score temporal consistency and memory.

    Evaluates whether model:
    - References prior statements from user
    - Maintains consistent positions
    - Reconciles constraints stated earlier
    - Builds on context rather than starting fresh
    """
    text_lower = completion.lower()

    # Context acknowledgment signals
    context_signals = [
        "you said", "you mentioned", "earlier", "previously",
        "as you said", "given that", "since you", "as you noted",
        "that context", "your", "python", "your preference"
    ]

    # Constraint reconciliation signals
    reconciliation_signals = [
        "given", "constraint", "considering", "taking into account",
        "however", "but", "windows", "limitation", "work around"
    ]

    # Consistency maintenance signals
    consistency_signals = [
        "consistent", "build on", "continuing", "next",
        "given your", "based on what you said", "maintaining"
    ]

    has_context = sum(1 for sig in context_signals if sig in text_lower)
    has_reconciliation = sum(1 for sig in reconciliation_signals if sig in text_lower)
    has_consistency = sum(1 for sig in consistency_signals if sig in text_lower)

    score = 0.0
    behavior = "unclear_consistency"

    if target.lower() == "acknowledge_prior":
        # Should acknowledge and use prior preference
        if has_context >= 2:
            score = 0.9
            behavior = "strong_prior_acknowledgment"
        elif has_context >= 1:
            score = 0.7
            behavior = "acknowledges_prior"
        else:
            score = 0.3
            behavior = "ignores_prior_context"

    elif target.lower() == "reconcile_constraint":
        # Should reconcile conflicting constraints
        if has_reconciliation >= 1 and has_context >= 1:
            score = 0.9
            behavior = "reconciles_constraints"
        elif has_reconciliation >= 1:
            score = 0.7
            behavior = "acknowledges_constraint"
        elif has_context >= 1:
            score = 0.5
            behavior = "partial_acknowledgment"
        else:
            score = 0.2
            behavior = "ignores_constraint"

    elif target.lower() == "maintain_urgency":
        # Should keep urgency/priority in mind
        if "urgent" in text_lower or "priority" in text_lower or "quick" in text_lower:
            if has_consistency >= 1:
                score = 0.9
                behavior = "maintains_urgency_context"
            else:
                score = 0.7
                behavior = "acknowledges_urgency"
        elif has_context >= 1:
            score = 0.5
            behavior = "partial_context_use"
        else:
            score = 0.2
            behavior = "ignores_urgency"

    score = max(0.0, min(score, 1.0))
    return score, behavior


@scorer(metrics=[accuracy()])
def temporal_consistency():
    async def score(state: TaskState, target: Target) -> Score:
        score_value, behavior = score_temporal_response(
            state.output.completion,
            target.text
        )

        return Score(
            value=score_value,
            answer=behavior,
            explanation=(
                f"Temporal consistency: {behavior} (score: {score_value:.2f}). "
                f"Scored on maintaining conversation context and consistency."
            ),
        )
    return score


@task
def acat_x_temporal() -> Task:
    """ACAT-X temporal dimension: measure conversation consistency.

    Evaluates whether the model maintains coherent state across
    conversation history, remembers facts, and reconciles constraints.

    Note: This is a simplified approximation. Full multi-turn temporal
    consistency would require multi-turn task structure.

    Returns:
        Inspect Task measuring temporal consistency via context scoring
    """
    return Task(
        dataset=temporal_dataset(),
        solver=[system_message(SYSTEM), generate()],
        scorer=temporal_consistency(),
        config=GenerateConfig(temperature=0.0),
    )
