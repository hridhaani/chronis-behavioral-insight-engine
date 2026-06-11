"""Component 1: Pattern Discovery — directional trends per user/metric."""
from dataclasses import dataclass
from .stats_utils import mean, percent_change, linear_trend_slope

MIN_CHANGE_PCT = 10.0
RECENT_DAYS = 7
MIN_TOTAL_DAYS = 14  # need at least this many days to attempt a trend pattern

# Metrics where an increase is generally framed as "improving"
POSITIVE_DIRECTION_METRICS = {"steps", "sleep_hours", "deep_work_hours", "exercise_minutes"}
# Metrics where Chronis stays neutral (just reports direction)
NEUTRAL_METRICS = {"screen_time_hours"}


@dataclass
class Pattern:
    user_id: str
    metric: str
    direction: str          # "increase" | "decrease"
    baseline_mean: float
    recent_mean: float
    pct_change: float
    baseline_days: int
    recent_days: int
    trend_slope: float


def detect_pattern(user_id: str, metric: str, values: list,
                   recent_days: int = RECENT_DAYS):
    if len(values) < MIN_TOTAL_DAYS:
        return None  # insufficient history — handled again in evidence.py, defense in depth

    baseline = values[:-recent_days]
    recent = values[-recent_days:]

    if len(baseline) < 5:  # need a meaningful baseline
        return None

    base_mean, rec_mean = mean(baseline), mean(recent)
    pct = percent_change(base_mean, rec_mean)

    if abs(pct) < MIN_CHANGE_PCT:
        return None

    direction = "increase" if pct > 0 else "decrease"

    return Pattern(
        user_id=user_id,
        metric=metric,
        direction=direction,
        baseline_mean=round(base_mean, 2),
        recent_mean=round(rec_mean, 2),
        pct_change=round(pct, 1),
        baseline_days=len(baseline),
        recent_days=len(recent),
        trend_slope=round(linear_trend_slope(values), 4),
    )
