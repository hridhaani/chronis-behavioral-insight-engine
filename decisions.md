# Decisions, Assumptions & Failure Modes

## Methodology

### Pattern Discovery
For each (user, metric) pair, we split the time series into a "baseline" window (all days
except the most recent 7) and a "recent" window (last 7 days). We compare the means of these
two windows. A pattern is reported only if the percentage change is at least 10% — this
threshold filters out everyday fluctuation and focuses on changes large enough to be
practically meaningful.

### Anomaly Detection
We compute a z-score for each day relative to that user's own mean and standard deviation for
that metric. Days with |z| >= 2.0 (roughly the top/bottom ~5% under a normal distribution) are
flagged as anomalies. Using per-user baselines (rather than population-wide thresholds) respects
that "normal" varies a lot between individuals.

### Confidence Scoring
- Pattern confidence blends (a) effect size — how large the change is relative to the user's
  typical variability — and (b) how much history is available. Both are normalized to [0, 1]
  and averaged, then capped at 0.95. We never report 1.0 confidence, reflecting irreducible
  uncertainty in a 30-day sample.
- Anomaly confidence scales with how extreme the z-score is beyond the 2.0 threshold.

### Evidence Sufficiency / Abstention
The system abstains (produces no insight, but logs why) when:
- Fewer than 14 days of data exist for a trend check, or fewer than 10 for an anomaly check.
- The percentage change for a potential pattern is below the 10% significance threshold.
- A metric's values are constant (zero variance), making "unusual" undefined.

We treat abstention as a first-class output, not an error — it demonstrates the system knows
the limits of its own evidence.

## Assumptions
- The dataset has no large gaps in dates per user (verified: 30 consecutive days for 5 users).
  If gaps existed, dates and values would need to be re-aligned via the date index rather than
  positional slicing.
- "Recent" is defined as the last 7 days of the dataset, which matches the example output in
  the assessment ("declined over the past week").
- Direction labels ("increase"/"decrease") are reported neutrally; we avoid stating a metric
  change is "good" or "bad" without domain context (e.g., more screen time isn't necessarily
  negative).
- Thresholds (10% change, z >= 2.0, 14/10-day minimums) are chosen as reasonable, explainable
  defaults appropriate for a 30-day synthetic dataset — not tuned against ground truth, since
  none was provided.

## Known Limitations / Failure Modes
- With only 30 days of data, statistical power is limited; confidence scores are intentionally
  capped at 0.95 to reflect this.
- The linear-trend slope is computed but only used as a secondary diagnostic; it is not
  currently surfaced in insight text. A future iteration could use it to describe acceleration
  ("the decline is accelerating") rather than just endpoint comparison.
- Z-score-based anomaly detection assumes roughly unimodal, not-too-skewed distributions per
  metric. With more data, a more robust measure (e.g., median absolute deviation) would be more
  resistant to the outliers it's trying to detect.
- The system analyzes each metric independently; it does not currently detect cross-metric
  patterns (e.g., "sleep dropped the same week screen time rose"). This was a deliberate scope
  cut to keep the system simple and explainable.
- If a user has any missing/non-numeric values, those rows are dropped before analysis, which
  could shift "recent window" boundaries slightly for that user. This is logged but not
  corrected for.
