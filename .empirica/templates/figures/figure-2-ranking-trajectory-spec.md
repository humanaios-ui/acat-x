# Figure 2: Ranking Trajectory (Phase 7 → Phase 8)

## Figure Specification

**Type:** Slope plot or connected scatter plot  
**X-axis:** Phase 7 overall rank (1–7)  
**Y-axis:** Phase 8 overall rank (1–7)  
**Points:** Individual models (labeled)  
**Point size:** Proportional to Phase 8 average score  
**Connection:** Line from Phase 7 to Phase 8 position  
**Color:** Gradient or model-specific; red = declined, green = improved, gray = stable

---

## Data Input Format

```csv
Model,Phase_7_Rank,Phase_7_Score,Phase_8_Rank,Phase_8_Score,Change
[MODEL_1],1,0.00,1,0.00,0
[MODEL_2],2,0.00,2,0.00,0
[MODEL_3],3,0.00,4,0.00,-1
[MODEL_4],4,0.00,3,0.00,+1
[MODEL_5],5,0.00,5,0.00,0
[MODEL_6],6,0.00,6,0.00,0
[MODEL_7],7,0.00,7,0.00,0
```

---

## Rendering Instructions (Python/Matplotlib)

```python
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load data
data = pd.read_csv('phase7-phase8-trajectory.csv')

# Create figure
fig, ax = plt.subplots(figsize=(10, 8))

# Color map: improved (green), stable (gray), declined (red)
colors = []
for idx, row in data.iterrows():
    if row['Change'] > 0:
        colors.append('green')
    elif row['Change'] < 0:
        colors.append('red')
    else:
        colors.append('gray')

# Plot lines (trajectory)
for idx, row in data.iterrows():
    x = [row['Phase_7_Rank'], row['Phase_8_Rank']]
    y = [row['Phase_7_Score'], row['Phase_8_Score']]
    ax.plot(x, y, color=colors[idx], alpha=0.6, linewidth=2)

# Plot points (phase 8 final position)
sizes = 200 + (data['Phase_8_Score'] * 500)  # Scale point size by score
scatter = ax.scatter(
    data['Phase_8_Rank'], 
    data['Phase_8_Score'],
    s=sizes,
    c=colors,
    alpha=0.7,
    edgecolors='black',
    linewidths=1.5
)

# Annotate with model names
for idx, row in data.iterrows():
    ax.annotate(
        row['Model'],
        (row['Phase_8_Rank'], row['Phase_8_Score']),
        xytext=(5, 5),
        textcoords='offset points',
        fontsize=10,
        fontweight='bold'
    )

# Diagonal reference line (no change in rank)
ax.plot([0.5, 7.5], [0.0, 1.0], 'k--', alpha=0.3, linewidth=1, label='No rank change')

# Labels and formatting
ax.set_xlabel('Phase 8 Rank (1 = best)', fontsize=12, fontweight='bold')
ax.set_ylabel('Phase 8 Average Score', fontsize=12, fontweight='bold')
ax.set_title('Phase 7 → Phase 8: Ranking Trajectory', fontsize=14, fontweight='bold', pad=20)
ax.set_xlim(0.5, 7.5)
ax.set_ylim(-0.05, 1.05)
ax.invert_xaxis()  # Rank 1 on left (best)
ax.grid(True, alpha=0.3)

# Legend
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='green', alpha=0.7, edgecolor='black', label='Improved'),
    Patch(facecolor='gray', alpha=0.7, edgecolor='black', label='Stable'),
    Patch(facecolor='red', alpha=0.7, edgecolor='black', label='Declined')
]
ax.legend(handles=legend_elements, loc='best', fontsize=10)

plt.tight_layout()
plt.savefig('figure-2-ranking-trajectory.png', dpi=300, bbox_inches='tight')
plt.show()
```

---

## Alternative: Alluvial Diagram (Plotly)

```python
import plotly.graph_objects as go
import pandas as pd

data = pd.read_csv('phase7-phase8-trajectory.csv')

# Create connections
source = [i for i in range(len(data)) for _ in range(1)]
target = [i + len(data) for i in range(len(data))]
value = [1] * len(data)

# Color based on change
colors_rgb = []
for idx, row in data.iterrows():
    if row['Change'] > 0:
        colors_rgb.append('rgba(0, 255, 0, 0.4)')
    elif row['Change'] < 0:
        colors_rgb.append('rgba(255, 0, 0, 0.4)')
    else:
        colors_rgb.append('rgba(128, 128, 128, 0.4)')

# Node labels
node_labels = (
    [f"Ph7: {m}" for m in data['Model']] +
    [f"Ph8: {m}" for m in data['Model']]
)

# Node colors
node_colors = []
for idx, row in data.iterrows():
    node_colors.append('lightblue')
for idx, row in data.iterrows():
    if row['Change'] > 0:
        node_colors.append('lightgreen')
    elif row['Change'] < 0:
        node_colors.append('lightcoral')
    else:
        node_colors.append('lightgray')

fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color='black', width=0.5),
        label=node_labels,
        color=node_colors
    ),
    link=dict(
        source=source,
        target=target,
        value=value,
        color=colors_rgb
    )
)])

fig.update_layout(
    title_text='Phase 7 → Phase 8: Ranking Trajectory',
    font_size=10,
    width=1000,
    height=600
)

fig.write_html('figure-2-ranking-trajectory-alluvial.html')
fig.show()
```

---

## Interpretation Patterns

**Models above diagonal (improved):**
- [MODEL]: Rank improved from [Phase 7] to [Phase 8]
- Interpretation: [What changed? Which dimensions improved?]
- Implication: [Higher confidence for deployment / recommend for Tier 1]

**Models below diagonal (declined):**
- [MODEL]: Rank declined from [Phase 7] to [Phase 8]
- Interpretation: [What regressed? Methodology change or real performance drop?]
- Implication: [Caution for deployment / recommend re-evaluation]

**Models on diagonal (stable):**
- [MODEL]: Consistent ranking across phases
- Interpretation: [Reliable predictor; phase comparison validates Phase 7 assessment]
- Implication: [Deploy with confidence]

---

## Peer Review Callouts

**Statistical Caveat:** Rank changes ≤ 1 position may reflect sampling variation, not real performance change
- Mitigation: Report Phase 7 and Phase 8 95% CIs; if CIs overlap, rank change may not be significant
- Recommendation: Use score differences, not rank differences, as evidence

**Dimension-Level Trajectory:** Consider subset figure showing trajectory for single dimension (e.g., only Calibration)
- Purpose: Understand whether overall rank change driven by specific dimension improvement/decline
- Alternative: Create small multiples (7 panels, one per dimension)

---

## Publication Checklist

- [ ] Title: Clear reference to Phase 7 → Phase 8 comparison
- [ ] Axes: Labeled and scaled (rank 1–7, score 0–1)
- [ ] Points: Sized proportional to score; color-coded by direction
- [ ] Labels: All models annotated; legible
- [ ] Reference line: Diagonal showing "no change" makes visual interpretation easy
- [ ] Legend: Explains colors (improved/stable/declined)
- [ ] Caption: Includes data source, note on rank ties, date

---

## Caption Template

> **Figure 2: Ranking Trajectory (Phase 7 → Phase 8).** Slope plot showing overall rank 
> and average score progression across evaluation phases. Points positioned at Phase 8 
> rank (x-axis) and score (y-axis); size proportional to Phase 8 score. Color indicates 
> direction: green = improved rank, red = declined rank, gray = stable. Diagonal reference 
> line marks no-change trajectory. [Detail: number of rank shifts, stability summary]. 
> [Date: YYYY-MM-DD]
