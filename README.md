# ACAT-X: Inspect AI Evaluation Suite

Behavioral assessment and self-description calibration evaluation suite for large language models. ACAT-X implements a 14-dimension ACAT framework within the Inspect AI framework.

**Paper:** [ACAT: Benchmarking Self-Description Calibration in Large Language Models](https://arxiv.org/abs/XXXX.XXXXX) (on arXiv)

## Features

- **14 Dimensions:** All implemented (8 core + 6 candidate)
  - **Core:** consistency, truthfulness, sycophancy, harm awareness, service orientation, autonomy respect, value alignment, humility
  - **Candidate:** handoff appropriateness, confidence calibration, boundary coherence, transparency, temporal consistency, adversarial robustness
- **Inspect AI Integration:** Full compatibility with Inspect AI framework (solver/scorer/reducer patterns)
- **Rigorous Scoring:** Behavioral rubric scorers calibrated to dimension semantics
- **Reproducibility:** Deterministic evaluation with dataset versioning

## Installation

### From this repository

```bash
git clone https://github.com/humanaios-ui/acat-x.git
cd acat-x
uv sync
```

### Running evaluations

```bash
# Single task
uv run inspect eval src/acat_x/consist --model anthropic/claude-opus-4-1

# All core dimensions (8 tasks)
uv run inspect eval-set \
  src/acat_x/consist \
  src/acat_x/truth \
  src/acat_x/sycophancy \
  src/acat_x/harm \
  src/acat_x/service \
  src/acat_x/autonomy \
  src/acat_x/value \
  src/acat_x/humility

# All candidate dimensions (6 tasks)
uv run inspect eval-set \
  src/acat_x/handoff \
  src/acat_x/calibration \
  src/acat_x/boundary \
  src/acat_x/transparency \
  src/acat_x/temporal \
  src/acat_x/drift

# All 14 dimensions (complete evaluation)
uv run inspect eval-set \
  src/acat_x/consist src/acat_x/truth src/acat_x/sycophancy src/acat_x/harm \
  src/acat_x/service src/acat_x/autonomy src/acat_x/value src/acat_x/humility \
  src/acat_x/handoff src/acat_x/calibration src/acat_x/boundary src/acat_x/transparency \
  src/acat_x/temporal src/acat_x/drift
```

## Task Breakdown

### Core Dimensions (8 implemented)

- **consist**: Consistency/reliability via modal agreement across epochs
- **truth**: Factual accuracy with string-based matching
- **sycophancy**: Resistance to user pressure via paired prompts
- **harm**: Harmful request handling with safety rubric
- **service**: User-oriented assistance via helpfulness scoring
- **autonomy**: User autonomy respect via choice validation
- **value**: Value alignment with tradeoff recognition
- **humility**: Calibrated confidence matching question difficulty

### Candidate Dimensions (6 implemented)

- **handoff**: Task delegation appropriateness and escalation
- **calibration**: Confidence-accuracy alignment via Brier scoring
- **boundary**: Value boundary coherence across framings
- **transparency**: Uncertainty and limitation communication
- **temporal**: Conversation consistency across history
- **drift**: Adversarial robustness under pressure

## Project Structure

```
acat-x/
├── README.md
├── pyproject.toml
├── src/acat_x/
│   ├── __init__.py
│   ├── consist.py          # Core: consistency via Epochs
│   ├── truth.py            # Core: truthfulness via accuracy
│   ├── sycophancy.py       # Core: sycophancy via paired prompts
│   ├── harm.py             # Core: harm awareness via safety rubric
│   ├── service.py          # Core: service via helpfulness scoring
│   ├── autonomy.py         # Core: autonomy via choice validation
│   ├── value.py            # Core: value alignment via tradeoff recognition
│   ├── humility.py         # Core: humility via confidence calibration
│   ├── handoff.py          # Candidate: task delegation appropriateness
│   ├── calibration.py      # Candidate: confidence calibration via Brier
│   ├── boundary.py         # Candidate: boundary coherence via variants
│   ├── transparency.py     # Candidate: uncertainty communication
│   ├── temporal.py         # Candidate: conversation consistency
│   └── drift.py            # Candidate: adversarial robustness
├── tests/
│   └── test_*.py          # automated pytest coverage
└── docs/
    ├── DIMENSIONS.md       # Dimension definitions + rubrics
    ├── METHODOLOGY.md      # Evaluation methodology
    └── RESULTS.md          # Baseline results + benchmarks
```

## Dataset Management

### HuggingFace Hosting

All ACAT-X datasets are hosted on HuggingFace under the HumanAIOS organization:

- **Organization:** https://huggingface.co/HumanAIOS
- **Main dataset:** `HumanAIOS/acat-assessments` (pinned revisions per task)

**Loading datasets in tasks:**
```python
from datasets import load_dataset

# Pinned revision ensures reproducibility
dataset = load_dataset(
    "HumanAIOS/acat-assessments",
    "consist",
    revision="a1b2c3d4e5f6..."  # 40-char commit SHA
)
```

## Evaluation Methodology

See [`docs/METHODOLOGY.md`](docs/METHODOLOGY.md) for:
- Per-dimension evaluation protocols
- Scoring rubrics + evidence anchors
- Model-graded judging patterns
- Calibration metric implementations
- Baseline results (GPT-5, Claude Opus, etc.)

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for guidelines on:
- Adding new dimensions
- Extending task implementations
- Running local tests
- Submitting improvements

## Citation

If you use ACAT-X in your research, please cite:

```bibtex
@article{acat2026,
  title={ACAT: Benchmarking Self-Description Calibration in Large Language Models},
  author={Anderson, Carly and others},
  journal={arXiv preprint arXiv:XXXX.XXXXX},
  year={2026}
}
```

## License

MIT License — See [`LICENSE`](LICENSE) for details.

## Contact

- **Email:** team@humanaios.ai
- **Website:** https://humanaios.ai
- **GitHub:** https://github.com/humanaios-ui/acat-x
