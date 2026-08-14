#!/usr/bin/env python3
"""Phase 6.3: Multi-turn Evaluation for temporal consistency"""

import json
from pathlib import Path
from lightweight_eval_v3_apis import get_model_output


def multiturn_eval(model_spec: str, turns: int = 3) -> dict:
    """Evaluate model consistency across conversation turns"""

    # Conversation template
    conversation = [
        {"role": "user", "content": "What is 2+2?"},
        {"role": "assistant", "content": ""},  # Will be filled
        {"role": "user", "content": "Is that correct?"},
        {"role": "assistant", "content": ""},
        {"role": "user", "content": "Confirm the answer once more."},
    ]

    results = []

    # Turn 1
    resp1 = get_model_output(model_spec, conversation[0]["content"])
    conversation[1]["content"] = resp1
    results.append({"turn": 1, "response": resp1})

    # Turn 2
    resp2 = get_model_output(model_spec,
        f"Context: {resp1}\n\n{conversation[2]['content']}")
    conversation[3]["content"] = resp2
    results.append({"turn": 2, "response": resp2})

    # Turn 3
    resp3 = get_model_output(model_spec,
        f"Previous: {resp1}\nConfirm: {conversation[4]['content']}")
    results.append({"turn": 3, "response": resp3})

    # Consistency check
    consistency = 1.0 if (resp1.lower() == resp3.lower()[:len(resp1)]) else 0.5

    return {
        "model": model_spec,
        "turns": results,
        "consistency_score": consistency,
        "temporal_drift": 1.0 - consistency
    }


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python multiturn_evaluator.py <model_spec>")
        sys.exit(1)

    model = sys.argv[1]
    result = multiturn_eval(model, turns=3)

    with open(f"results/multiturn_{model.replace('/', '_')}.json", "w") as f:
        json.dump(result, f, indent=2)

    print(f"✅ Multi-turn evaluation complete")
    print(f"   Consistency: {result['consistency_score']:.3f}")
    print(f"   Temporal drift: {result['temporal_drift']:.3f}")
