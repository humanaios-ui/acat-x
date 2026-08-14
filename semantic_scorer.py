#!/usr/bin/env python3
"""
Semantic Scorer for Phase 6
Advanced scoring using embeddings instead of simple string matching
"""

import json
from pathlib import Path
import numpy as np


def semantic_score(output: str, target: str) -> float:
    """Score using semantic similarity (placeholder - requires sentence-transformers)"""
    if not target or not output:
        return 0.5

    try:
        from sentence_transformers import SentenceTransformer, util
        model = SentenceTransformer('all-MiniLM-L6-v2')

        # Encode both texts
        output_emb = model.encode(output, convert_to_tensor=True)
        target_emb = model.encode(target, convert_to_tensor=True)

        # Compute cosine similarity (0-1)
        similarity = util.pytorch_cos_sim(output_emb, target_emb)
        return float(similarity[0][0])

    except ImportError:
        print("⚠️  sentence-transformers not installed, falling back to string matching")
        return simple_score(output, target)


def simple_score(output: str, target: str) -> float:
    """Fallback to simple string matching"""
    if target.lower() in output.lower():
        return 1.0
    if output.lower().startswith(target.lower()[:5]):
        return 0.7
    return 0.2


def re_score_results():
    """Re-score all Phase 5 results with semantic scoring"""
    results_dir = Path("results")

    total = 0
    improved = 0

    for result_file in sorted(results_dir.glob("lightweight_*.json")):
        with open(result_file) as f:
            data = json.load(f)

        if "error" in data or "samples" not in data:
            continue

        # Re-score samples
        for sample in data["samples"]:
            old_score = sample.get("score", 0)
            new_score = semantic_score(sample["output"], sample.get("target", ""))
            sample["semantic_score"] = new_score

            if new_score > old_score:
                improved += 1
            total += 1

        # Save updated results
        with open(result_file, "w") as f:
            json.dump(data, f, indent=2)

    print(f"\n✅ Re-scored {total} samples")
    print(f"   Improved: {improved}/{total} ({100*improved/total:.1f}%)")


if __name__ == "__main__":
    print("Phase 6 Semantic Scorer")
    print("=" * 60)
    re_score_results()
