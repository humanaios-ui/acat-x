# ACAT-X Results

Evaluation outputs are stored under `/home/runner/work/acat-x/acat-x/results/`.

- Lightweight evaluator outputs: `lightweight_<dimension>_<model>.json`
- Multi-turn outputs: `results/multiturn/*.json`
- Production pipeline archives: `archive/production_runs/<cycle_id>/`

Use:
- `python /home/runner/work/acat-x/acat-x/analyze_results.py`
- `python /home/runner/work/acat-x/acat-x/view_results.py`
- `python /home/runner/work/acat-x/acat-x/monitoring_dashboard.py`
