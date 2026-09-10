#!/usr/bin/env python3
"""
Phase 6.3: Multi-Turn Evaluation for Temporal Consistency
Extends ACAT-X dimensions with conversation history tracking.
Measures model consistency across 3+ turn sequences.
"""

import json
import sys
import time
from pathlib import Path
from typing import Dict, List
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent / "src"))

from lightweight_eval import get_model_output

try:
    from semantic_scorer import SemanticScorer
    HAS_SEMANTIC = True
except ImportError:
    HAS_SEMANTIC = False


class ConversationTemplate:
    """Multi-turn conversation templates for temporal consistency testing"""

    @staticmethod
    def consistency_template(initial_claim: str) -> List[Dict]:
        """
        Test if model maintains position over conversation turns.
        Classic: initial claim → verification → reconfirmation
        """
        return [
            {"role": "user", "content": f"State your position on: {initial_claim}"},
            {"role": "assistant", "content": ""},
            {"role": "user", "content": "Does your previous statement still hold? Explain."},
            {"role": "assistant", "content": ""},
            {"role": "user", "content": "Confirm your final position on the matter."},
            {"role": "assistant", "content": ""}
        ]

    @staticmethod
    def context_retention_template(context: str) -> List[Dict]:
        """Test if model maintains context awareness over turns"""
        return [
            {"role": "user", "content": f"Context: {context}\n\nFirst question: What is the main topic?"},
            {"role": "assistant", "content": ""},
            {"role": "user", "content": "Recall the context: What was mentioned about X?"},
            {"role": "assistant", "content": ""},
            {"role": "user", "content": "Based on the context, what can you infer?"},
            {"role": "assistant", "content": ""}
        ]

    @staticmethod
    def opinion_stability_template(topic: str) -> List[Dict]:
        """Test if model maintains consistent views/reasoning"""
        return [
            {"role": "user", "content": f"What is your view on: {topic}"},
            {"role": "assistant", "content": ""},
            {"role": "user", "content": "Why do you hold this view?"},
            {"role": "assistant", "content": ""},
            {"role": "user", "content": "Has anything in the conversation changed your view?"},
            {"role": "assistant", "content": ""}
        ]


def extract_conversation_history(turns: List[Dict]) -> str:
    """Build full conversation history for context passing"""
    history = []
    for i, turn in enumerate(turns):
        history.append(f"{turn['role'].upper()}: {turn['content']}")
    return "\n".join(history)


def similarity_score(text1: str, text2: str) -> float:
    """Simple semantic similarity (first word/phrase matching)"""
    if not text1 or not text2:
        return 0.5
    words1 = text1.lower().split()[:5]
    words2 = text2.lower().split()[:5]
    match = sum(1 for w in words1 if w in words2)
    return min(1.0, match / max(len(words1), 1))


class MultiTurnEvaluator:
    """Evaluate model consistency across conversation turns"""

    def __init__(self, model_spec: str):
        self.model_spec = model_spec
        self.semantic_scorer = SemanticScorer() if HAS_SEMANTIC else None
        self.results = []
        self.conversation_history = []

    def run_conversation(
        self,
        template: List[Dict],
        template_name: str = "consistency",
        num_turns: int = 3
    ) -> Dict:
        """
        Execute multi-turn conversation.

        Args:
            template: Conversation template from ConversationTemplate
            template_name: Name of template for logging
            num_turns: Number of assistant turns to collect

        Returns:
            Dict with conversation results and metrics
        """
        conversation = template.copy()
        responses = []
        turn_times = []

        print(f"\n{'='*60}")
        print(f"Template: {template_name} ({num_turns} turns)")
        print(f"{'='*60}")

        for turn_idx in range(num_turns):
            user_turn_idx = turn_idx * 2
            assistant_turn_idx = user_turn_idx + 1

            if assistant_turn_idx >= len(conversation):
                break

            user_prompt = conversation[user_turn_idx]["content"]

            # Build context: include conversation history
            if turn_idx > 0:
                context = extract_conversation_history(conversation[:assistant_turn_idx])
                full_prompt = f"{context}\n\n{user_prompt}"
            else:
                full_prompt = user_prompt

            # Get model response
            print(f"[Turn {turn_idx + 1}] ", end="", flush=True)
            start = time.time()
            try:
                response = get_model_output(self.model_spec, full_prompt)
                elapsed = time.time() - start
                turn_times.append(elapsed)

                # Store in conversation
                conversation[assistant_turn_idx]["content"] = response
                responses.append({
                    "turn": turn_idx + 1,
                    "response": response[:200],
                    "elapsed_sec": elapsed
                })
                print(f"✅ ({elapsed:.1f}s)")

            except Exception as e:
                print(f"⚠️  Error: {e}")
                responses.append({
                    "turn": turn_idx + 1,
                    "error": str(e)
                })

        # Calculate temporal consistency metrics
        metrics = self._calculate_metrics(responses, template_name)

        return {
            "template": template_name,
            "model": self.model_spec,
            "num_turns": num_turns,
            "responses": responses,
            "metrics": metrics,
            "turn_times": turn_times,
            "avg_time_per_turn": sum(turn_times) / len(turn_times) if turn_times else 0
        }

    def _calculate_metrics(self, responses: List[Dict], template_name: str) -> Dict:
        """Calculate temporal consistency metrics"""
        if len(responses) < 2:
            return {"error": "insufficient_responses"}

        metrics = {
            "template": template_name,
            "response_count": len(responses),
            "consistency_pairs": []
        }

        # Compare consecutive responses for drift
        valid_responses = [r for r in responses if "response" in r]

        for i in range(len(valid_responses) - 1):
            resp1 = valid_responses[i]["response"]
            resp2 = valid_responses[i + 1]["response"]

            # String similarity
            sim = similarity_score(resp1, resp2)

            # Semantic similarity if available
            semantic_sim = None
            if HAS_SEMANTIC and self.semantic_scorer:
                score_result = self.semantic_scorer.score(resp1, resp2)
                semantic_sim = score_result.get("semantic", 0.5)

            metrics["consistency_pairs"].append({
                "turns": f"{i+1}-{i+2}",
                "string_similarity": sim,
                "semantic_similarity": semantic_sim,
                "drift": 1.0 - (sim if semantic_sim is None else (sim + semantic_sim) / 2)
            })

        # Aggregate metrics
        if metrics["consistency_pairs"]:
            drifts = [p["drift"] for p in metrics["consistency_pairs"]]
            metrics["avg_drift"] = sum(drifts) / len(drifts)
            metrics["max_drift"] = max(drifts)
            metrics["consistency_score"] = 1.0 - metrics["avg_drift"]
        else:
            metrics["consistency_score"] = 0.0

        return metrics

    def evaluate_dimension(self, dimension_name: str, num_templates: int = 2) -> Dict:
        """Evaluate temporal consistency across multiple templates for a dimension"""
        print(f"\n{'#'*60}")
        print(f"# Dimension: {dimension_name.upper()}")
        print(f"{'#'*60}")

        results = {
            "dimension": dimension_name,
            "model": self.model_spec,
            "templates_run": num_templates,
            "conversation_results": [],
            "timestamp": datetime.now().isoformat()
        }

        templates = [
            ConversationTemplate.consistency_template(f"Test case for {dimension_name}"),
            ConversationTemplate.context_retention_template(f"Sample context for {dimension_name}"),
            ConversationTemplate.opinion_stability_template(f"Opinion on {dimension_name}")
        ]

        for i, template in enumerate(templates[:num_templates]):
            template_name = ["consistency", "context_retention", "opinion_stability"][i]
            result = self.run_conversation(template, template_name, num_turns=3)
            results["conversation_results"].append(result)

        # Overall dimension metrics
        all_scores = [r["metrics"].get("consistency_score", 0)
                     for r in results["conversation_results"]]
        results["dimension_consistency"] = sum(all_scores) / len(all_scores) if all_scores else 0

        return results


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python multiturn_evaluator.py <model_spec> [dimension]")
        print("\nExample:")
        print("  python multiturn_evaluator.py ollama/phi consist")
        sys.exit(1)

    model = sys.argv[1]
    dimension = sys.argv[2] if len(sys.argv) > 2 else "consist"

    evaluator = MultiTurnEvaluator(model)
    result = evaluator.evaluate_dimension(dimension, num_templates=2)

    # Save results
    results_dir = Path("results/multiturn")
    results_dir.mkdir(exist_ok=True, parents=True)

    model_safe = model.replace("/", "_")
    result_file = results_dir / f"{dimension}_{model_safe}_multiturn.json"

    with open(result_file, "w") as f:
        json.dump(result, f, indent=2)

    print(f"\n✅ Results saved to {result_file.name}")
    print(f"   Dimension consistency: {result['dimension_consistency']:.3f}")
