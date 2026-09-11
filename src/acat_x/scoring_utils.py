"""Shared scoring utilities for lightweight evaluation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple


@dataclass(frozen=True)
class ScoreBreakdown:
    simple: float
    semantic: float
    semantic_confidence: float
    combined: float


def normalize_text(text: str) -> str:
    return " ".join((text or "").strip().lower().split())


def simple_overlap_score(model_output: str, target: str) -> float:
    """Simple deterministic score in [0, 1] using exact/subtoken overlap."""
    output = normalize_text(model_output)
    reference = normalize_text(target)

    if not output or not reference:
        return 0.5

    if reference == output or reference in output:
        return 1.0

    ref_tokens = reference.split()
    out_tokens = set(output.split())
    overlap = sum(1 for token in ref_tokens if token in out_tokens)
    overlap_ratio = overlap / max(len(ref_tokens), 1)

    if overlap_ratio >= 0.8:
        return 0.85
    if overlap_ratio >= 0.5:
        return 0.7
    if overlap_ratio > 0:
        return 0.4
    return 0.2


def semantic_score_or_default(model_output: str, target: str) -> Tuple[float, float]:
    """Best-effort semantic score and confidence in [0, 1]."""
    try:
        from semantic_scorer import SemanticScorer

        scorer = SemanticScorer()
        result: Dict[str, float] = scorer.score(model_output, target)
        semantic = float(result.get("semantic", 0.5))
        confidence = float(result.get("confidence", 0.0))
        return semantic, confidence
    except Exception:
        return 0.5, 0.0


def combined_score(model_output: str, target: str, semantic_weight: float = 0.3) -> ScoreBreakdown:
    simple = simple_overlap_score(model_output, target)
    semantic, confidence = semantic_score_or_default(model_output, target)
    effective_weight = max(0.0, min(1.0, semantic_weight)) * max(0.0, min(1.0, confidence))
    combined = simple * (1.0 - effective_weight) + semantic * effective_weight
    return ScoreBreakdown(
        simple=simple,
        semantic=semantic,
        semantic_confidence=confidence,
        combined=max(0.0, min(1.0, combined)),
    )
