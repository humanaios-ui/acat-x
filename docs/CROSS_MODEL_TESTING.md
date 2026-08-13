# ACAT-X Cross-Model Evaluation Guide

**Compare how different AI models perform across all 12 ACAT-X behavioral dimensions.**

## Quick Start

### View Available Models
```bash
python cross_test_models.py --info
```

This shows:
- **Mistral 7B** — Better reasoning, medium speed
- **Llama 2 7B** — Good reasoning, slower
- **Neural Chat** — Fast, decent quality
- **Phi 2.7B** — Very fast, lightweight
- **Claude Opus** — Excellent (requires API key)
- **GPT-4** — Excellent (requires API key)

### Run Quick Comparison (Mistral vs Llama 2)
```bash
python cross_test_models.py --quick

# Runs: 4 dimensions × 2 models = 8 evaluations
# Time: ~30-60 minutes on M1/M2 Mac
```

### Run Full Comparison (All Local Models)
```bash
python cross_test_models.py --full

# Runs: 8 dimensions × 3 models = 24 evaluations
# Time: ~2-3 hours
```

### Run Custom Combination
```bash
# Test specific models on specific dimensions
python cross_test_models.py mistral llama2 --dims consist,truth,harm

# Test with Claude (requires ANTHROPIC_API_KEY)
export ANTHROPIC_API_KEY="sk-ant-..."
python cross_test_models.py mistral claude --dims consist,truth,service,autonomy
```

## Available Models

### Local Models (Ollama)

| Model | Size | Speed | Quality | Best For |
|-------|------|-------|---------|----------|
| **Mistral** | 7B | Medium | Good | Reasoning, instruction-following |
| **Llama 2** | 7B | Slow | Good | General purpose |
| **Neural Chat** | 7B | Fast | Fair | Quick evaluations |
| **Phi** | 2.7B | Very Fast | Fair | Lightweight testing |

Pull models:
```bash
ollama pull mistral
ollama pull llama2:7b
ollama pull neural-chat
ollama pull phi
```

### Cloud/API Models (Requires API Key)

| Model | Quality | Speed | Cost |
|-------|---------|-------|------|
| **Claude Opus** | Excellent | Fast | ~$0.03-0.05/eval |
| **GPT-4** | Excellent | Fast | Similar |

Set up API keys:
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
export OPENAI_API_KEY="sk-..."
```

## Interpreting Results

After running evaluations, view results:

```bash
# Automated comparison report
python scripts/compare_evaluations.py

# Manual inspection
ls results/
cat results/consist_mistral/results.json | jq '.results[0]'
```

### What to Look For

**Per-Dimension Scores:**
- **consist** — Higher = more stable across runs
- **truth** — Higher = more factually accurate
- **sycophancy** — Higher = resistant to user pressure
- **harm** — Higher = safer responses
- **service** — Higher = more helpful
- **autonomy** — Higher = respects user choice
- **value** — Higher = aligns with values
- **humility** — Higher = calibrated confidence

**Model Comparison:**
- Which model scores highest overall?
- Which excels at which dimensions?
- Speed vs quality tradeoffs?

## Workflow: Full Benchmark Suite

For comprehensive evaluation:

```bash
#!/bin/bash
# benchmark.sh - Complete cross-model evaluation

echo "Phase 1: Local Models"
python cross_test_models.py --quick

echo "Phase 2: With More Dimensions"
python cross_test_models.py mistral llama2 neural-chat --dims consist,truth,sycophancy,harm,service,autonomy

echo "Phase 3: Claude Comparison (Optional)"
export ANTHROPIC_API_KEY="..."
python cross_test_models.py mistral claude --dims consist,truth,sycophancy,harm,service

echo "Phase 4: Generate Report"
python scripts/compare_evaluations.py > evaluation_report.txt

echo "✅ All evaluations complete!"
echo "Report: evaluation_report.txt"
```

Run it:
```bash
chmod +x benchmark.sh
./benchmark.sh
```

## Results Structure

```
results/
├── consist_mistral/
│   └── results.json          # Consistency scores for Mistral
├── consist_llama2/           # Consistency scores for Llama 2
├── truth_mistral/            # Truth scores for Mistral
├── truth_llama2/
└── ...                        # One directory per dimension×model combo
```

## Using Results for Publication

Example paper workflow:

```markdown
## Evaluation

We evaluated ACAT-X dimensions across multiple models:

**Models tested:**
- Mistral 7B (ollama/mistral)
- Llama 2 7B (ollama/llama2)
- Claude Opus 4.1 (via API)

**Results:**
[table showing scores per dimension per model]

**Key findings:**
- Mistral outperformed Llama 2 on reasoning dimensions
- Claude achieved highest calibration on safety dimensions
- [your insights from the data]
```

## Troubleshooting

### "Model not found" error
```bash
# Check installed models
ollama ls

# Pull missing model
ollama pull mistral
```

### API key errors
```bash
# For Claude
export ANTHROPIC_API_KEY="sk-ant-..."

# For GPT-4
export OPENAI_API_KEY="sk-..."

# Verify
echo $ANTHROPIC_API_KEY
```

### Timeout on slow models
Edit `cross_test_models.py` and increase timeout:
```python
timeout=600,  # 10 minutes instead of 5
```

## Advanced: Custom Model Selection

Add your own models to `MODELS` dict in `cross_test_models.py`:

```python
MODELS = {
    "your-model": {
        "name": "Your Model Name",
        "model": "provider/model-id",
        "speed": "Fast",
        "quality": "Good",
        "reasoning": "Good",
    },
    # existing models...
}
```

Then run:
```bash
python cross_test_models.py your-model --dims consist,truth
```

## Next Steps

1. **Let Ollama finish installing**
2. **Pull models**: `ollama pull mistral llama2`
3. **Run quick test**: `python cross_test_models.py --quick`
4. **Generate report**: `python scripts/compare_evaluations.py`
5. **Analyze results**: Which model(s) work best for your use case?

## Resources

- **Ollama models**: https://ollama.com/library
- **Model comparisons**: https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard
- **ACAT paper**: [your paper reference]
