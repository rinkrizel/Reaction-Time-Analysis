
# RT Analysis (Python)

A small, beginner-friendly behavioral data analysis project focused on reaction-time (RT) data.
It demonstrates practical steps that are common in cognitive/behavioral research:
data simulation, RT cleaning, summary metrics, and clear visualizations.

## What this project includes
- Synthetic RT dataset (subjects × trials × conditions)
- Standard RT cleaning rules (removing implausibly fast/slow responses)
- Summary tables (mean/median RT, accuracy) per condition
- Visualizations (distributions, condition effects, speed–accuracy tradeoff)

## Why RT cleaning matters
RT datasets often include lapses, accidental presses, and outliers. Clean preprocessing improves interpretability
and prevents misleading conclusions.

## How to run
```bash
pip install -r requirements.txt
python3 analysis.py
