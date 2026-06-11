"""Component 2: Anomaly Detection — per-user z-score outliers."""
from dataclasses import dataclass
from .stats_utils import mean, std, z_scores

Z_THRESHOLD = 2.0
MIN_HISTORY_FOR_ANOMALY = 10  # need enough history for std dev to be meaningful


@dataclass
class Anomaly:
    user_id: str
    metric: str
    date: str
    value: float
    z_score: float
    user_mean: float
    user_std: float


def detect_anomalies(user_id: str, metric: str, dates: list,
                     values: list,
                     z_threshold: float = Z_THRESHOLD) -> list:
    if len(values) < MIN_HISTORY_FOR_ANOMALY:
        return []

    if std(values) == 0:
        return []  # no variance -> nothing is "unusual"

    zs = z_scores(values)
    m, s = mean(values), std(values)

    anomalies = []
    for date, val, z in zip(dates, values, zs):
        if abs(z) >= z_threshold:
            anomalies.append(Anomaly(
                user_id=user_id,
                metric=metric,
                date=str(date),
                value=val,
                z_score=round(z, 2),
                user_mean=round(m, 2),
                user_std=round(s, 2),
            ))
    return anomalies
