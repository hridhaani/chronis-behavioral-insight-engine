# Chronis Behavioral Insight Engine

A small, explainable system that turns daily behavioral logs (steps, sleep, screen time,
deep work, exercise) into evidence-backed insights: trends, anomalies, and confidence-scored
findings — with abstention when evidence is weak.

## Quick Start

```bash
pip install -r requirements.txt
python run.py --data data/Chronis_TaskA_Data_v2-2.csv --out outputs/
```

## What it does

1. **Pattern Discovery** — detects meaningful (>=10%) shifts between baseline and recent behavior.
2. **Anomaly Detection** — flags single days that are statistically unusual for that person.
3. **Insight Generation** — produces a human-readable insight string + evidence dict + confidence score.
4. **Evidence Sufficiency** — abstains (with a logged reason) when data is too sparse or the signal is too weak to support a claim.

## Project layout

```
chronis-behavioral-insights/
├── README.md
├── requirements.txt
├── decisions.md
├── run.py                        # single entry point: python run.py
├── data/
│   └── Chronis_TaskA_Data_v2-2.csv
├── src/
│   ├── __init__.py
│   ├── data_loader.py            # load + validate CSV
│   ├── stats_utils.py            # shared math helpers (mean, std, z-score, slope)
│   ├── pattern_detection.py      # Component 1
│   ├── anomaly_detection.py      # Component 2
│   ├── confidence.py             # Component 3 helper
│   ├── evidence.py               # Component 4 helper
│   └── insight_generator.py      # Component 3 — orchestrates everything
├── outputs/
│   ├── insights_report.json
│   └── insights_report.md
├── examples/
│   └── sample_output.md
└── tests/
    ├── test_pattern_detection.py
    ├── test_anomaly_detection.py
    └── test_insight_generator.py
```

## Running tests

```bash
pytest
```

## Output

`run.py` writes two files to `outputs/`:

- `insights_report.json` — machine-readable, one object per insight with `type`, `user_id`, `metric`, `insight`, `confidence`, and `evidence`.
- `insights_report.md` — human-readable rollup grouped by user, followed by an abstentions section.

It also prints a one-line summary to stdout, e.g.:

```
Generated 14 insights, abstained on 31 checks.
Reports written to outputs/
```

## Design choices

See `decisions.md` for the full rationale behind thresholds, confidence formulas, and known limitations.
