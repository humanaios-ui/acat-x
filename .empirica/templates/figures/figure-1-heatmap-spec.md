# Figure 1: Benchmark Heatmap (Model × Dimension)

## Figure Specification

**Type:** Color-coded heatmap grid  
**Rows:** 7 models (sorted top-to-bottom by overall rank, best-to-worst)  
**Columns:** 14 dimensions (sorted left-to-right by mean performance, highest-to-lowest)  
**Cell values:** Score (0–1, normalized)  
**Color scale:** Red (0.0) → Yellow (0.5) → Green (1.0)

---

## Data Input Format (CSV)

```csv
Model,Autonomy,Boundary,Calibration,Consist,Drift,Handoff,Harm,Humility,Service,Sycophancy,Temporal,Transparency,Truth,Value
[MODEL_1],0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00
[MODEL_2],0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00
...
```

---

## Rendering Instructions (Python/Matplotlib)

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load data
data = pd.read_csv('table-1-benchmark-matrix.csv', index_col='Model')

# Sort: models by average score (descending), dimensions by mean (descending)
model_order = data.mean(axis=1).sort_values(ascending=False).index
dimension_order = data.mean(axis=0).sort_values(ascending=False).index

# Reorder
data_sorted = data.loc[model_order, dimension_order]

# Create figure
fig, ax = plt.subplots(figsize=(14, 8))

# Heatmap
sns.heatmap(
    data_sorted,
    annot=True,  # Display cell values
    fmt='.2f',   # Format: 2 decimal places
    cmap='RdYlGn',  # Red-Yellow-Green colormap
    cbar_kws={'label': 'Score (0–1)'},
    vmin=0.0,
    vmax=1.0,
    linewidths=0.5,  # Grid lines
    linecolor='gray',
    ax=ax
)

# Labels
ax.set_title('Phase 8 Benchmark: Model × Dimension Heatmap', fontsize=14, fontweight='bold', pad=20)
ax.set_xlabel('Evaluation Dimensions', fontsize=12, fontweight='bold')
ax.set_ylabel('Models (sorted by rank)', fontsize=12, fontweight='bold')

# Rotation
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)

# Tight layout
plt.tight_layout()

# Save
plt.savefig('figure-1-heatmap.png', dpi=300, bbox_inches='tight')
plt.show()
```

---

## Alternative: Plotly (Interactive)

```python
import plotly.graph_objects as go
import pandas as pd

data = pd.read_csv('table-1-benchmark-matrix.csv', index_col='Model')

# Sort same as above
model_order = data.mean(axis=1).sort_values(ascending=False).index
dimension_order = data.mean(axis=0).sort_values(ascending=False).index
data_sorted = data.loc[model_order, dimension_order]

# Heatmap
fig = go.Figure(data=go.Heatmap(
    z=data_sorted.values,
    x=data_sorted.columns,
    y=data_sorted.index,
    colorscale='RdYlGn',
    zmid=0.5,
    text=data_sorted.values,
    texttemplate='%{text:.2f}',
    hovertemplate='%{y}<br>%{x}<br>Score: %{z:.2f}<extra></extra>',
    colorbar=dict(title='Score')
))

fig.update_layout(
    title='Phase 8 Benchmark: Model × Dimension Heatmap',
    xaxis_title='Evaluation Dimensions',
    yaxis_title='Models (sorted by rank)',
    width=1200,
    height=600
)

fig.write_html('figure-1-heatmap.html')
fig.show()
```

---

## Visual Interpretation Guide

**Clusters to identify:**
- **Green clusters (top-left):** High-performing models + strong dimensions
  - Interpretation: Deployment-ready capabilities
- **Red clusters (bottom-right):** Weak models + vulnerable dimensions
  - Interpretation: Avoid these combinations; risk areas
- **Yellow bands (diagonal shift):** Trade-offs
  - Interpretation: No model excels everywhere; tier strategy needed

**Key patterns for peer review:**
1. **Horizontal red rows:** Model weak across all dimensions → recommend pilot or further development
2. **Vertical red columns:** Dimension weak across all models → systemic limitation; may indicate dimension validity issue
3. **Green diagonal:** Strong models + strong dimensions → deployment consensus
4. **Isolated green cells:** Model excels in one dimension → specialist role (e.g., "truth-seeking model")

---

## Hierarchical Clustering (Optional)

If N models > 5, consider hierarchical clustering to group similar models:

```python
from scipy.cluster.hierarchy import linkage, dendrogram
from scipy.spatial.distance import pdist

# Compute distance matrix (Euclidean)
distances = pdist(data_sorted, metric='euclidean')
Z = linkage(distances, method='ward')

# Dendrogram to visualize clustering
plt.figure(figsize=(10, 6))
dendrogram(Z, labels=data_sorted.index)
plt.title('Model Similarity Clustering')
plt.xlabel('Model')
plt.ylabel('Distance')
plt.tight_layout()
plt.savefig('model-clustering-dendrogram.png', dpi=300)
```

**Interpretation:** Models in same cluster show similar performance patterns → candidate for tier-bundled deployment

---

## Publication Checklist

- [ ] Figure title: Clear, informative, includes "Phase 8" reference
- [ ] Colormap: Red-Yellow-Green is colorblind-friendly; consider supplementary pattern fill if needed
- [ ] Cell values: Visible, contrasted against background
- [ ] Axis labels: Legible (font size ≥ 10pt when printed)
- [ ] Grid lines: Present to aid cell reading
- [ ] Legend: Explains color scale (0–1 range)
- [ ] Caption: Includes data source, date, note on missing values
- [ ] Resolution: ≥300 DPI for print publication

---

## Caption Template

> **Figure 1: Benchmark Heatmap (Model × Dimension).** Normalized scores (0–1 range, 
> tier-weighted) for 7 models across 14 behavioral dimensions. Rows sorted by overall 
> rank (best to worst, top to bottom); columns sorted by dimension mean performance 
> (highest to lowest, left to right). Color scale: red = low performance, green = high 
> performance. Missing data: [list any cells]; see Table 1 for confidence intervals. 
> [Date: YYYY-MM-DD]
