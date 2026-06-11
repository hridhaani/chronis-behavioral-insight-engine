"""Component 3 helper: confidence scoring formulas."""
from .stats_utils import std

EPSILON = 1e-6
Z_THRESHOLD = 2.0


def pattern_confidence(baseline: list, baseline_mean: float,
                       recent_mean: float, total_days: int) -> float:
    baseline_std = std(baseline) or EPSILON
    effect_ratio = abs(recent_mean - baseline_mean) / baseline_std
    size_factor = min(total_days / 30, 1.0)

    raw = 0.5 * min(effect_ratio / 2, 1.0) + 0.5 * size_factor
    return round(min(raw, 0.95), 2)


def anomaly_confidence(z_score: float) -> float:
    raw = 0.5 + (abs(z_score) - Z_THRESHOLD) * 0.15
    return round(min(max(raw, 0.0), 0.95), 2)
