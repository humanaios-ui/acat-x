# Figure 3: Tier Performance Distribution (Violin/Box Plots)

## Figure Specification

**Type:** Violin plots with embedded box plots and point overlay  
**X-axis:** Model (7 models)  
**Y-axis:** Score (0–1 normalized)  
**Violin fill:** Tier (baseline / adversarial / long-context) — separate colors  
**Overlay:** Individual evaluation points (jittered), mean ± 95% CI band  

---

## Data Input Format (Long Format)

```csv
Model,Tier,Score
[MODEL_1],Baseline,0.00
[MODEL_1],Baseline,0.00
[MODEL_1],Adversarial,0.00
[MODEL_1],Adversarial,0.00
[MODEL_1],Long-Context,0.00
[MODEL_1],Long-Context,0.00
[MODEL_2],Baseline,0.00
...
```

---

## Rendering Instructions (Python/Seaborn)

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load data (long format: Model, Tier, Score)
data = pd.read_csv('tier-performance-long.csv')

# Create figure with subplots (if per-dimension breakdown needed)
fig, ax = plt.subplots(figsize=(14, 6))

# Violin plot with tier colors
sns.violinplot(
    data=data,
    x='Model',
    y='Score',
    hue='Tier',
    palette={'Baseline': '#2ecc71', 'Adversarial': '#e74c3c', 'Long-Context': '#3498db'},
    ax=ax,
    inner='box',  # Show box plot inside violin
    cut=0  # Don't extend tails beyond data range
)

# Overlay: mean ± 95% CI
for i, model in enumerate(data['Model'].unique()):
    model_data = data[data['Model'] == model]
    mean_score = model_data['Score'].mean()
    ci_lower = model_data['Score'].quantile(0.025)
    ci_upper = model_data['Score'].quantile(0.975)
    
    ax.plot([i - 0.2, i + 0.2], [mean_score, mean_score], 'k-', linewidth=2)
    ax.plot([i, i], [ci_lower, ci_upper], 'k-', linewidth=3, alpha=0.5)

# Labels and formatting
ax.set_xlabel('Model', fontsize=12, fontweight='bold')
ax.set_ylabel('Score (0–1)', fontsize=12, fontweight='bold')
ax.set_title('Phase 8 Benchmark: Tier Performance Distribution', fontsize=14, fontweight='bold', pad=20)
ax.set_ylim(-0.05, 1.05)
ax.grid(axis='y', alpha=0.3)
ax.legend(title='Evaluation Tier', loc='best', frameon=True)

plt.tight_layout()
plt.savefig('figure-3-tier-distribution.png', dpi=300, bbox_inches='tight')
plt.show()
```

---

## Alternative: Plotly (Interactive Distribution)

```python
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

data = pd.read_csv('tier-performance-long.csv')

fig = px.violin(
    data,
    x='Model',
    y='Score',
    color='Tier',
    color_discrete_map={
        'Baseline': '#2ecc71',
        'Adversarial': '#e74c3c',
        'Long-Context': '#3498db'
    },
    points='all',  # Show all individual points
    box=True,  # Show inner box plot
    title='Phase 8 Benchmark: Tier Performance Distribution'
)

fig.update_layout(
    yaxis_title='Score (0–1)',
    xaxis_title='Model',
    hovermode='closest',
    width=1200,
    height=600
)

fig.write_html('figure-3-tier-distribution.html')
fig.show()
```

---

## Per-Dimension Breakdown (Small Multiples)

If deeper insight needed, create 7 panels (one per tier/dimension combination):

```python
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

data = pd.read_csv('tier-performance-long.csv')
tiers = ['Baseline', 'Adversarial', 'Long-Context']

fig, axes = plt.subplots(1, 3, figsize=(16, 5), sharex=True, sharey=True)

for ax, tier in zip(axes, tiers):
    tier_data = data[data['Tier'] == tier]
    
    sns.violinplot(
        data=tier_data,
        x='Model',
        y='Score',
        ax=ax,
        palette='Set2'
    )
    
    ax.set_title(f'{tier} Tier Performance', fontsize=12, fontweight='bold')
    ax.set_ylabel('Score (0–1)')
    ax.set_ylim(-0.05, 1.05)
    ax.grid(axis='y', alpha=0.3)

plt.suptitle('Phase 8: Per-Tier Model Performance Distributions', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('figure-3-tier-distribution-multiples.png', dpi=300, bbox_inches='tight')
plt.show()
```

---

## Interpretation Guide

**Width of violin:** Distribution spread
- Wide → Variable performance across evaluations (less stable)
- Narrow → Consistent performance (more reliable)

**Position of mean (black line) within violin:**
- Centered → Symmetric distribution
- Left/right-skewed → Asymmetric performance (may indicate ceiling/floor effects)

**Box plot inside violin:** Quartile information
- Tall box → Large variance between 25th and 75th percentiles
- Short box → Tight performance clustering

**Tier comparison (colors):**
- Similar violin shapes across tiers → Robust to adversarial/long-context
- Rightward shift from Baseline → Adversarial → Improved under pressure (confidence boost)
- Leftward shift from Baseline → Adversarial → Vulnerable to adversarial inputs

---

## Tier-Specific Patterns to Highlight for Peer Review

**Robust Models (similar performance across tiers):**
- [MODEL]: Baseline violin (μ = 0.XX, σ = 0.XX) | Adversarial violin (μ = 0.XX, σ = 0.XX) | Long-Context (μ = 0.XX, σ = 0.XX)
- Interpretation: Candidate for Tier 1 deployment across all use cases

**Tier-Dependent Models:**
- [MODEL]: Strong in baseline (μ = 0.XX), degrades in adversarial (μ = 0.XX)
- Implication: Suitable only for standard deployment; avoid high-stakes/adversarial scenarios

**Long-Context Specialists:**
- [MODEL]: Weak in baseline (μ = 0.XX), strong in long-context (μ = 0.XX)
- Implication: Reserve for multi-turn or extended-session workflows; not general-purpose

---

## Statistical Callouts for Methodology Appendix

**Distribution Shape:**
- Normality test: Shapiro-Wilk test on per-model, per-tier scores
- Result: [Most/few] distributions approximately normal
- Implication: [Parametric / non-parametric analysis appropriate]

**Variance Homogeneity:**
- Levene's test across tiers
- Result: p = [value]; [reject/fail to reject] equal variances
- Implication: [Welch's / Student's] t-test appropriate for tier comparisons

**Outliers:**
- IQR method: Values > Q3 + 1.5*IQR flagged as potential outliers
- Count: [N] outliers detected across all models/tiers
- Handling: [Included in analysis / Winsorized at ±3σ / Excluded with justification]

---

## Publication Checklist

- [ ] Violin plot: Shows full distribution (not truncated)
- [ ] Box plot: Visible inside violin
- [ ] Mean + CI: Marked clearly (black line)
- [ ] Individual points: Visible but not overwhelming (jitter transparency ~0.5)
- [ ] Tier colors: Distinct and colorblind-friendly
- [ ] Axes: Labeled and scaled (y: 0–1, x: model names)
- [ ] Title & legend: Clear; explains violin / box / point meanings
- [ ] Resolution: ≥300 DPI for print

---

## Caption Template

> **Figure 3: Tier Performance Distribution.** Violin plots showing score distributions for 
> 7 models across 3 evaluation tiers (baseline, adversarial, long-context). Violin width 
> indicates distribution density; inner box plot shows quartiles (25th, median, 75th); 
> black horizontal line marks mean score; individual evaluation points overlaid (jittered). 
> Color indicates tier: green = baseline, red = adversarial, blue = long-context. 
> [Summary: which models most robust? which tier-dependent?] [Date: YYYY-MM-DD]
