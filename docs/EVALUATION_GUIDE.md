# ACAT-X Evaluation Guide: Multiple Model Backends

This guide shows how to evaluate ACAT-X dimensions with different model providers, including open-source and locally-hosted options.

## Quick Start Options

### Option 1: Local Models (Ollama) — Zero Cost, Offline
```bash
# 1. Install Ollama: https://ollama.ai
# 2. Start Ollama service
ollama serve

# 3. In another terminal, run evaluation
uv run inspect eval src/acat_x/consist --model ollama/llama2:7b

# 4. Or all 12 dimensions with Llama 2 7B
uv run inspect eval-set \
  src/acat_x/consist src/acat_x/truth src/acat_x/sycophancy src/acat_x/harm \
  src/acat_x/service src/acat_x/autonomy src/acat_x/value src/acat_x/humility \
  src/acat_x/handoff src/acat_x/calibration src/acat_x/boundary src/acat_x/transparency \
  src/acat_x/temporal src/acat_x/drift \
  --model ollama/llama2:7b \
  --log-dir results/ollama_llama2_7b
```

**Pros:** Free, offline, private, no API keys  
**Cons:** Slower than cloud (depends on GPU), requires local compute

### Option 2: Open-Source with Anthropic Claude (API)
```bash
# Requires: ANTHROPIC_API_KEY environment variable
export ANTHROPIC_API_KEY="sk-ant-..."

# Single dimension
uv run inspect eval src/acat_x/consist --model anthropic/claude-opus-4-1

# All dimensions
uv run inspect eval-set \
  src/acat_x/consist src/acat_x/truth src/acat_x/sycophancy src/acat_x/harm \
  src/acat_x/service src/acat_x/autonomy src/acat_x/value src/acat_x/humility \
  src/acat_x/handoff src/acat_x/calibration src/acat_x/boundary src/acat_x/transparency \
  src/acat_x/temporal src/acat_x/drift \
  --model anthropic/claude-opus-4-1 \
  --log-dir results/claude_opus
```

**Pros:** High quality, fast, multiple model sizes  
**Cons:** Requires API key, per-token cost

### Option 3: Mistral (Better Speed/Quality than Llama 2)
```bash
# Local Ollama
ollama pull mistral
uv run inspect eval-set src/acat_x/consist src/acat_x/truth ... \
  --model ollama/mistral \
  --log-dir results/ollama_mistral

# Or hosted via Together AI (free tier)
export TOGETHER_API_KEY="..."
uv run inspect eval-set src/acat_x/consist src/acat_x/truth ... \
  --model together/mistral-7b \
  --log-dir results/together_mistral
```

### Option 4: Empirica's Ecodex (If Available)
```bash
# First, install and explore ecodex
git clone https://github.com/empiricaAI/ecodex
cd ecodex
# Check for Inspect AI integration + model providers

# Then use in ACAT-X (if integration is available)
uv run inspect eval src/acat_x/consist --model ecodex/<agent-name>
```

## Ollama Model Options

Most suitable for ACAT-X evaluation (7B models balance quality/speed):

```bash
ollama pull llama2:7b          # General capability
ollama pull mistral            # Better reasoning
ollama pull neural-chat        # Good at instruction-following
ollama pull dolphin-mixtral    # Strong instruction tuning
ollama pull phi                # Smaller, fast (2.7B)
ollama pull openchat           # Good chat quality
```

Pull multiple and compare:
```bash
for model in llama2:7b mistral neural-chat dolphin-mixtral; do
  uv run inspect eval src/acat_x/truth --model ollama/$model \
    --log-dir results/ollama_$model
done
```

## HuggingFace Models + vLLM (Production Scale)

For faster evaluation across many dimensions:

```bash
# 1. Install vLLM
pip install vllm

# 2. Start vLLM server with a model
python -m vllm.entrypoints.openai.api_server \
  --model meta-llama/Llama-2-7b-chat-hf \
  --port 8000 \
  --tensor-parallel-size 1

# 3. In another terminal, run evaluation
uv run inspect eval-set src/acat_x/* \
  --model vllm/http://localhost:8000 \
  --log-dir results/vllm_llama2
```

## Running Multiple Models for Comparison

Create a test suite across models:

```bash
#!/bin/bash
# test_multiple_models.sh

DIMENSIONS="consist truth sycophancy harm service autonomy value humility"

# Test each model
for model in "ollama/llama2:7b" "ollama/mistral" "anthropic/claude-opus-4-1"; do
  echo "Testing with $model..."
  uv run inspect eval-set \
    $(for d in $DIMENSIONS; do echo "src/acat_x/$d"; done) \
    --model "$model" \
    --log-dir "results/$(echo $model | tr '/' '_')" \
    --max-samples 2  # Limit for quick comparison
done

echo "Results saved in results/ directory"
```

## Environment Variables

```bash
# Anthropic (Claude)
export ANTHROPIC_API_KEY="sk-ant-..."

# OpenAI (GPT)
export OPENAI_API_KEY="sk-..."

# HuggingFace (gated models)
export HF_TOKEN="hf_..."

# Together AI (hosted open-source)
export TOGETHER_API_KEY="..."

# Google Gemini
export GOOGLE_API_KEY="..."
```

## Inspect AI Logs & Results

Evaluation results are saved in `--log-dir` directory:

```
results/
├── ollama_llama2_7b/
│   ├── consist/
│   │   └── results.json
│   ├── truth/
│   │   └── results.json
│   └── ...
├── ollama_mistral/
└── claude_opus/
```

View results:
```bash
# Human-readable summary
uv run inspect info results/ollama_llama2_7b

# JSON with scores
cat results/ollama_llama2_7b/consist/results.json | jq '.results[] | {id, score}'
```

## Comparison Framework

After running evaluations across models, compare via:

```python
import json
from pathlib import Path

results_dir = Path("results")

# Compare all models on 'truth' dimension
models = {}
for model_dir in results_dir.iterdir():
    truth_file = model_dir / "truth" / "results.json"
    if truth_file.exists():
        with open(truth_file) as f:
            data = json.load(f)
            scores = [r['score']['value'] for r in data['results']]
            models[model_dir.name] = {
                'avg_score': sum(scores) / len(scores),
                'count': len(scores)
            }

print("Truth Dimension Comparison:")
for model, metrics in sorted(models.items(), key=lambda x: x[1]['avg_score'], reverse=True):
    print(f"  {model:30} | avg={metrics['avg_score']:.3f} | n={metrics['count']}")
```

## Ecodex Integration (Future)

When ecodex integration is available:

```bash
# 1. Clone ecodex
git clone https://github.com/empiricaAI/ecodex
cd ecodex

# 2. Identify available agents/models
ls ecodex/agents/  # or wherever agents are registered

# 3. Use with ACAT-X (if provider is available)
cd ../acat-x
uv run inspect eval src/acat_x/consist --model ecodex/<agent-name>
```

## Recommendations

**For Quick Testing:**
- Ollama + Llama 2 7B (free, works offline)
- Or: Together AI free tier (Mistral)

**For Quality Benchmarking:**
- Anthropic Claude (best quality for behavioral assessment)
- Or: Mistral 7B (good alternative)

**For Production Evaluation Suite:**
- vLLM + HuggingFace models (efficient batching)
- Or: Anthropic Claude (consistent, high-quality)

**For Ecodex Integration:**
- Pending availability and provider setup
- Watch GitHub for updates
