"""Small, dependency-light statistical helpers used across detectors."""
import numpy as np


def mean(values):
    return float(np.mean(values)) if len(values) else float("nan")


def std(values):
    # ddof=1 -> sample std dev; guard against tiny samples
    return float(np.std(values, ddof=1)) if len(values) > 1 else 0.0


def z_scores(values):
    m, s = mean(values), std(values)
    if s == 0:
        return [0.0] * len(values)
    return [(v - m) / s for v in values]


def percent_change(old, new):
    if old == 0:
        return float("inf") if new != 0 else 0.0
    return (new - old) / old * 100.0


def linear_trend_slope(values):
    """Slope of best-fit line over index 0..n-1. Positive = increasing trend."""
    if len(values) < 2:
        return 0.0
    x = np.arange(len(values))
    slope, _ = np.polyfit(x, values, 1)
    return float(slope)
