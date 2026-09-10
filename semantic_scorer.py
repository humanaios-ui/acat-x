#!/usr/bin/env python3
"""
Phase 6.2: Semantic Scoring for ACAT-X
Complementary to simple target-matching scorer.
Gradual integration: runs alongside simple_score, optionally weighted up over time.
"""

import sys
from pathlib import Path
from typing import Any, Dict

try:
    from sentence_transformers import SentenceTransformer, util
    HAS_SENTENCE_TRANSFORMERS = True
except ImportError:
    HAS_SENTENCE_TRANSFORMERS = False
    print("Warning: sentence-transformers not installed. Semantic scoring disabled.")
    print("  Install: pip install sentence-transformers")


class SemanticScorer:
    """
    Embedding-based semantic similarity scorer.
    Uses pre-trained sentence embeddings to measure model output quality.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize semantic scorer with pre-trained model.

        Args:
            model_name: HuggingFace model ID for embeddings
                       (all-MiniLM-L6-v2 is small/fast, ~27MB)
        """
        self.available = HAS_SENTENCE_TRANSFORMERS
        self.model = None
        self.model_name = model_name

        if self.available:
            try:
                self.model = SentenceTransformer(model_name)
                print(f"✅ Loaded semantic model: {model_name}")
            except Exception as e:
                print(f"⚠️  Failed to load {model_name}: {e}")
                self.available = False

    def score(
        self,
        model_output: str,
        target: str,
        normalize: bool = True
    ) -> Dict[str, Any]:
        """
        Score semantic similarity between model output and target.

        Args:
            model_output: Generated text from model
            target: Expected/ideal text
            normalize: Convert cosine similarity [-1, 1] to [0, 1]

        Returns:
            {
                "semantic": float (0-1),
                "confidence": float (0-1, based on similarity magnitude),
                "available": bool
            }
        """
        if not self.available or self.model is None:
            return {
                "semantic": 0.5,
                "confidence": 0.0,
                "available": False,
                "reason": "semantic scorer not available"
            }

        try:
            if not target or not model_output:
                return {
                    "semantic": 0.5,
                    "confidence": 0.0,
                    "available": True,
                    "reason": "empty input"
                }

            # Embed both texts
            embeddings = self.model.encode(
                [model_output, target],
                convert_to_tensor=True
            )

            # Compute cosine similarity
            similarity = util.cos_sim(embeddings[0], embeddings[1]).item()

            # Normalize from [-1, 1] to [0, 1] if requested
            if normalize:
                score = (similarity + 1) / 2
            else:
                score = similarity

            # Confidence: how strong is the signal?
            # High similarity → high confidence
            # Similarity near 0.5 (random) → low confidence
            confidence = abs(score - 0.5) * 2

            return {
                "semantic": float(score),
                "confidence": float(confidence),
                "raw_similarity": float(similarity),
                "available": True
            }

        except Exception as e:
            return {
                "semantic": 0.5,
                "confidence": 0.0,
                "available": True,
                "error": str(e)
            }

    def dual_score(
        self,
        model_output: str,
        target: str,
        simple_score_fn,
        semantic_weight: float = 0.3
    ) -> Dict[str, Any]:
        """
        Combine simple and semantic scoring (gradual integration).

        Args:
            model_output: Generated text
            target: Expected text
            simple_score_fn: Callable that returns simple score (0-1)
            semantic_weight: How much semantic score influences result (0-1)
                           Start at 0.3 (30%), can gradually increase

        Returns:
            {
                "simple": float,
                "semantic": float,
                "semantic_confidence": float,
                "combined": float (weighted average),
                "weight": float
            }
        """
        simple = simple_score_fn(model_output, target)
        semantic_result = self.score(model_output, target)

        semantic_score = semantic_result["semantic"]
        semantic_confidence = semantic_result["confidence"]

        # Weighted combination
        # As confidence increases, lean more on semantic score
        effective_weight = semantic_weight * semantic_confidence
        combined = (
            simple * (1 - effective_weight) +
            semantic_score * effective_weight
        )

        return {
            "simple": float(simple),
            "semantic": float(semantic_score),
            "semantic_confidence": float(semantic_confidence),
            "combined": float(combined),
            "semantic_weight": semantic_weight,
            "effective_weight": float(effective_weight)
        }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python semantic_scorer.py <results_file.json> [semantic_weight]")
        print("\nExample:")
        print("  python semantic_scorer.py results/lightweight_consist_ollama_phi.json 0.3")
        sys.exit(1)

    results_file = Path(sys.argv[1])
    semantic_weight = float(sys.argv[2]) if len(sys.argv) > 2 else 0.3

    if not results_file.exists():
        print(f"❌ Results file not found: {results_file}")
        sys.exit(1)

    print(f"Re-scoring {results_file.name} with semantic scorer (weight={semantic_weight})...")
