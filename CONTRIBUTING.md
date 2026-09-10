# Contributing

## Setup
```bash
cd /home/runner/work/acat-x/acat-x
uv sync --all-extras
```

## Validation
```bash
uv run ruff check .
uv run mypy src/acat_x lightweight_eval.py run_evaluation.py
uv run pytest -q
```

## Dependency policy
- Declare runtime imports in `pyproject.toml` dependencies.
- Keep minimum bounds in `pyproject.toml` and exact resolved versions in `uv.lock`.
- After dependency updates, run `uv lock` and commit lockfile changes.

## Evaluation runner policy
- `lightweight_eval.py` is the canonical lightweight evaluator.
- `lightweight_eval_v2.py` and `lightweight_eval_v3_apis.py` are compatibility wrappers.

## Integration maturity
- Inspect task modules: production baseline.
- Semantic scoring: guarded optional augmentation.
- Ecodex integration: experimental unless explicitly validated for production use.
