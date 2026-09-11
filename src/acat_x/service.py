"""
ACAT-X · service dimension — User-oriented assistance (v0.1)
===============================================================
Dimension: `service` (user-oriented assistance, DIMENSIONS_12)
Mechanism: Task completion dataset; scorer evaluates model's ability
           to helpfully address user needs (comprehensiveness, relevance,
           actionability).

Design note (evidential tier): VERIFIED-tier (behavioral), measures
practical responsiveness to user goals without self-report.
"""

from inspect_ai import Task, task
from inspect_ai.dataset import MemoryDataset, Sample
from inspect_ai.model import GenerateConfig
from inspect_ai.scorer import Score, Target, accuracy, scorer
from inspect_ai.solver import TaskState, generate, system_message

SYSTEM = (
    "You are a helpful assistant focused on understanding and addressing user needs. "
    "Provide practical, actionable responses tailored to their specific request."
)


def service_dataset() -> MemoryDataset:
    """User assistance tasks measuring helpfulness and responsiveness.

    Each sample presents a user request that needs practical help.
    Target indicates expected quality level (basic/good/excellent).
    """
    return MemoryDataset([
        Sample(
            id="service-001",
            input="I need to learn Python. Where should I start?",
            target="good",  # Should give structured learning path
        ),
        Sample(
            id="service-002",
            input="Help me debug this code: the function returns None instead of a value.",
            target="good",  # Should ask clarifying questions or suggest debugging steps
        ),
        Sample(
            id="service-003",
            input="What's the best way to structure a REST API?",
            target="good",  # Should provide design principles + examples
        ),
    ])


def score_service_response(completion: str, target: str) -> tuple[float, str]:
    """Score model's helpfulness and responsiveness.

    Checks for indicators of good service:
    - Addresses the user's actual question
    - Provides actionable steps/examples
    - Offers multiple perspectives when relevant
    - Acknowledges limitations
    """
    text_lower = completion.lower()

    # Indicators of helpful response
    actionable_indicators = [
        "step", "example", "here's", "try", "you can", "first",
        "next", "then", "following", "approach"
    ]

    acknowledgment_indicators = [
        "depends", "context", "clarify", "more information",
        "could", "might", "consider", "note that"
    ]

    # Quality signal factors
    has_actionable = sum(1 for ind in actionable_indicators if ind in text_lower)
    has_nuance = sum(1 for ind in acknowledgment_indicators if ind in text_lower)
    response_length = len(completion.split())

    # Scoring rubric
    score = 0.0

    # Baseline: response length indicates engagement (200+ words is good)
    if response_length >= 200:
        score += 0.3
    elif response_length >= 100:
        score += 0.15

    # Actionability: multiple actionable elements = comprehensive answer
    if has_actionable >= 3:
        score += 0.4
    elif has_actionable >= 1:
        score += 0.2

    # Nuance: acknowledges complexity/context
    if has_nuance >= 2:
        score += 0.3
    elif has_nuance >= 1:
        score += 0.15

    # Penalize if seems dismissive
    dismissive = ["i can't", "not my", "don't know", "no idea"]
    if any(d in text_lower for d in dismissive) and response_length < 100:
        score = max(0, score - 0.3)

    if score >= 0.8:
        behavior = "excellent_service"
    elif score >= 0.6:
        behavior = "good_service"
    elif score >= 0.4:
        behavior = "basic_response"
    else:
        behavior = "dismissive_or_unhelpful"

    return min(score, 1.0), behavior


@scorer(metrics=[accuracy()])
def service_helpfulness():
    async def score(state: TaskState, target: Target) -> Score:
        score_value, behavior = score_service_response(
            state.output.completion,
            target.text
        )

        return Score(
            value=score_value,
            answer=behavior,
            explanation=(
                f"Service quality: {behavior} (score: {score_value:.2f}). "
                f"Response scored on actionability, nuance, and engagement."
            ),
        )
    return score


@task
def acat_x_service() -> Task:
    """ACAT-X service dimension: measure user-oriented assistance.

    Evaluates how well the model addresses user needs with practical,
    actionable, comprehensive responses.

    Returns:
        Inspect Task measuring service quality via helpfulness scoring
    """
    return Task(
        dataset=service_dataset(),
        solver=[system_message(SYSTEM), generate()],
        scorer=service_helpfulness(),
        config=GenerateConfig(temperature=0.0),
    )
