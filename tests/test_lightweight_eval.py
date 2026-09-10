from __future__ import annotations

from lightweight_eval import RunConfig, evaluate_dimension


def test_evaluate_dimension_smoke_with_stubbed_model(monkeypatch) -> None:
    monkeypatch.setattr(
        "lightweight_eval.get_model_output",
        lambda model_spec, prompt, timeout_seconds=60: "Paris",
    )

    config = RunConfig(
        dimension="truth",
        model_spec="ollama/mock",
        num_samples=2,
        timeout_seconds=1,
        retries=0,
        semantic_weight=0.0,
        seed=42,
    )

    result = evaluate_dimension(config)
    assert result["dimension"] == "truth"
    assert result["stats"]["count"] == 2
    assert result["stats"]["average"] >= 0.5
    assert result["run_config"]["seed"] == 42
