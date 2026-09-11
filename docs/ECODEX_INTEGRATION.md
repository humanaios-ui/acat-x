# ACAT-X + Ecodex Integration Guide

**Maturity:** Experimental integration path (not yet production-hardened).

**ecodex** is Empirica's epistemic-discipline agent fork. It measures what it knows using the same discipline framework as empirica CLI, making it ideal for evaluating ACAT-X with proper calibration tracking.

## Why Ecodex for ACAT-X?

| Feature | Benefit |
|---------|---------|
| **Epistemic Discipline** | ACAT-X measures model behavior; ecodex measures what it knows about its own behavior |
| **Multi-Model Support** | Hot-swap between Ollama, Claude, GPT, Mistral, Deepseek mid-session |
| **Cross-AI Mesh** | Receives proposals from empirica, participates in multi-agent evaluations |
| **Calibration History** | Tracks divergence between stated vs actual accuracy across evaluation runs |
| **Curated Model Registry** | Pre-filtered, capability-tagged models (not 300-model dump) |

## Installation

### Option 1: Install Script (Recommended)
```bash
curl -fsSL https://raw.githubusercontent.com/EmpiricaAI/ecodex/main/scripts/install.sh | bash
```

### Option 2: Homebrew
```bash
brew install EmpiricaAI/tap/ecodex
```

### Option 3: From Source (Rust devs)
```bash
cargo install --git https://github.com/EmpiricaAI/ecodex codex-cli
```

**Prerequisites:**
- Empirica CLI: `brew install EmpiricaAI/tap/empirica` or equivalent
- For local models: Ollama, llama.cpp, vLLM, or LM Studio

### Verify Installation
```bash
ecodex --version
empirica --version
```

## Ollama Setup (Local Models)

### Mac Installation (Detailed Steps)

The install script sometimes has issues on M1/M2 Macs. Here's the manual approach:

```bash
# 1. Download Ollama for Mac directly (easier than script)
# Visit: https://ollama.com/download/Ollama-darwin.zip
# Or via CLI:
curl -L -o ~/Downloads/Ollama-darwin.zip https://ollama.com/download/Ollama-darwin.zip
unzip ~/Downloads/Ollama-darwin.zip -d /Applications

# 2. Verify installation
/Applications/Ollama.app/Contents/bin/ollama --version

# 3. Add to PATH
echo 'export PATH="/Applications/Ollama.app/Contents/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# 4. Start Ollama service
ollama serve
# This starts the API on http://localhost:11434
```

### Or: Use Homebrew (Simpler)
```bash
brew install ollama
brew services start ollama
# Verify: curl http://localhost:11434/api/tags
```

### Pull Models
```bash
ollama pull llama2:7b      # General capability (4GB)
ollama pull mistral         # Better reasoning (4GB)
ollama pull neural-chat     # Instruction tuning (4GB)
```

### Verify Ollama is Running
```bash
# Should return {"models": [...]}
curl http://localhost:11434/api/tags | jq

# Or test a simple inference
curl http://localhost:11434/api/generate -d '{"model":"llama2","prompt":"hello"}'
```

## Using Ecodex with ACAT-X

### Launch Ecodex
```bash
ecodex
```

This opens the TUI. On first run:
1. `/model` → Select a model provider (Ollama, Claude, etc.)
2. `/model ollama/llama2` → Switch to Llama 2 7B

### Run ACAT-X Evaluation in Ecodex

Ecodex is primarily a code editor/agent. To evaluate ACAT-X with ecodex:

```bash
# 1. Inside ecodex terminal, navigate to ACAT-X
cd ~/practices/acat-x

# 2. Have ecodex run the evaluation
@ecodex run an evaluation on the consist dimension using Inspect AI
```

Or directly via inspect from within an ecodex session:

```bash
# Inside ecodex
uv run inspect eval src/acat_x/consist --model ollama/llama2:7b
```

### Ecodex Model Hot-Swap
Press `/model` during a session to change models mid-conversation:
- `ollama/llama2:7b` → Local Llama 2
- `ollama/mistral` → Local Mistral
- `anthropic/claude-opus-4-1` → Claude (requires API key)
- `openai/gpt-4` → GPT-4 (requires API key)

No restart needed.

## Configuration

### Provider Setup

Ecodex comes with curated defaults. Add API keys as environment variables:

```bash
# Anthropic
export ANTHROPIC_API_KEY="sk-ant-..."

# OpenAI
export OPENAI_API_KEY="sk-..."

# Together AI (hosted open-source)
export TOGETHER_API_KEY="..."

# Ollama: automatically works if running on localhost:11434
# No API key needed
```

### Ecodex Config File
`~/.ecodex/config.toml` (auto-created on first run)

View available models:
```toml
[model]
# Ollama models (auto-discovered)
# Claude models via Anthropic API
# GPT models via OpenAI API
# etc.
```

## Bridging ACAT-X ↔ Ecodex

### Architecture
```
ACAT-X Tasks (Inspect AI)
      ↓
  [Model Provider API]
      ↓
    Ecodex
      ↓
  [Epistemic Discipline + Calibration]
```

### Workflow

**1. Run ACAT-X with Ecodex Agent:**
```bash
# Start ecodex session
ecodex

# Inside ecodex, request evaluation
@ecodex Please evaluate the consist dimension of ACAT-X using llama2:7b

# ecodex runs: uv run inspect eval src/acat_x/consist --model ollama/llama2:7b
# Measures its own epistemic state while running the evaluation
```

**2. Get Calibration Feedback:**
Ecodex logs PREFLIGHT/POSTFLIGHT for the evaluation session, measuring:
- `know` — Understanding of the evaluation task
- `uncertainty` — Calibrated confidence in results
- `completion` — Progress through evaluation
- `clarity` — Clarity of what's being measured

**3. Cross-Model Comparison in Ecodex:**
```bash
# Have ecodex run comparative evaluations
@ecodex Compare ACAT-X results across three models:
1. ollama/llama2:7b
2. ollama/mistral
3. anthropic/claude-opus-4-1 (if API key available)

# ecodex orchestrates the runs and logs calibration deltas
```

## Mesh Participation (Advanced)

Ecodex can participate in the Empirica cross-AI mesh:

```bash
# In ecodex
@ecodex Check if there are any proposals in my inbox related to ACAT-X evaluation
```

Ecodex can:
- **Receive proposals** from Claude Code or other agents
- **Poll inbox** for work requests
- **Send proposals** back to other agents
- **Coordinate** evaluations across multiple AIs

## Troubleshooting

### Ollama Not Responding
```bash
# Check if Ollama is running
lsof -i :11434

# Start Ollama if not running
ollama serve

# Or if installed via Homebrew:
brew services restart ollama
```

### Model Not Found
```bash
# List available models
ollama ls

# Pull a model
ollama pull mistral

# Verify in Ecodex: /model
```

### Ecodex Won't Start
```bash
# Ensure empirica CLI is on PATH
which empirica

# If not found, install
brew install EmpiricaAI/tap/empirica
```

### API Key Issues
```bash
# Test API key before using
export ANTHROPIC_API_KEY="sk-ant-..."
curl https://api.anthropic.com/v1/health -H "x-api-key: $ANTHROPIC_API_KEY"
```

## Next Steps

1. **Install Ollama:** `brew install ollama && brew services start ollama`
2. **Install Ecodex:** `curl ... | bash` (see above)
3. **Pull a model:** `ollama pull llama2`
4. **Launch Ecodex:** `ecodex`
5. **Set model:** `/model ollama/llama2:7b`
6. **Test ACAT-X:** `cd ~/practices/acat-x && uv run inspect eval src/acat_x/consist --model ollama/llama2:7b`

## Resources

- **Ecodex Docs:** https://github.com/EmpiricaAI/ecodex/tree/main/docs/ecodex
- **Ollama:** https://ollama.com
- **Empirica:** https://empirica.ai
- **Inspect AI:** https://github.com/UKGovernmentBEIS/inspect_ai
