"""Component 3: Insight Generation — orchestrates detection + scoring into final reports."""
from .data_loader import get_user_series, NUMERIC_COLUMNS
from .pattern_detection import detect_pattern, POSITIVE_DIRECTION_METRICS
from .anomaly_detection import detect_anomalies
from .evidence import check_trend_evidence, check_anomaly_evidence
from .confidence import pattern_confidence, anomaly_confidence

METRIC_LABELS = {
    "steps": "daily steps",
    "sleep_hours": "sleep duration",
    "screen_time_hours": "screen time",
    "deep_work_hours": "deep work hours",
    "exercise_minutes": "exercise minutes",
}


def _pattern_to_insight(p, baseline_values):
    label = METRIC_LABELS[p.metric]
    verb = "increased" if p.direction == "increase" else "decreased"
    text = (f"{label.capitalize()} for {p.user_id} {verb} from an average of "
            f"{p.baseline_mean} to {p.recent_mean} over the last {p.recent_days} days "
            f"({p.pct_change:+.1f}%).")
    confidence = pattern_confidence(baseline_values, p.baseline_mean, p.recent_mean,
                                    p.baseline_days + p.recent_days)
    return {
        "type": "pattern",
        "user_id": p.user_id,
        "metric": p.metric,
        "insight": text,
        "confidence": confidence,
        "evidence": {
            "baseline_mean": p.baseline_mean,
            "recent_mean": p.recent_mean,
            "pct_change": p.pct_change,
            "baseline_days": p.baseline_days,
            "recent_days": p.recent_days,
        },
    }


def _anomaly_to_insight(a):
    label = METRIC_LABELS[a.metric]
    direction = "higher" if a.z_score > 0 else "lower"
    text = (f"On {a.date}, {a.user_id}'s {label} was {a.value}, which is unusually {direction} "
            f"compared to their typical average of {a.user_mean} "
            f"(z-score = {a.z_score}).")
    return {
        "type": "anomaly",
        "user_id": a.user_id,
        "metric": a.metric,
        "insight": text,
        "confidence": anomaly_confidence(a.z_score),
        "evidence": {
            "date": a.date,
            "value": a.value,
            "user_mean": a.user_mean,
            "user_std": a.user_std,
            "z_score": a.z_score,
        },
    }


def generate_insights(df) -> dict:
    insights = []
    abstentions = []

    for user_id in sorted(df["user_id"].unique()):
        for metric in NUMERIC_COLUMNS:
            values = get_user_series(df, user_id, metric)
            dates = df.loc[df["user_id"] == user_id, "date"].dt.strftime("%Y-%m-%d").tolist()
            # align dates with non-null values (simple approach: assume no gaps in this dataset;
            # for production, join on index after dropna — see decisions.md)

            # --- Pattern (trend) ---
            trend_check = check_trend_evidence(values)
            if not trend_check.sufficient:
                abstentions.append({
                    "user_id": user_id, "metric": metric, "type": "pattern",
                    "reason": trend_check.reason,
                })
            else:
                pattern = detect_pattern(user_id, metric, values)
                if pattern:
                    baseline_values = values[:-pattern.recent_days]
                    insights.append(_pattern_to_insight(pattern, baseline_values))
                else:
                    abstentions.append({
                        "user_id": user_id, "metric": metric, "type": "pattern",
                        "reason": "Change in recent average did not exceed the "
                                  "10% significance threshold.",
                    })

            # --- Anomalies ---
            anomaly_check = check_anomaly_evidence(values)
            if not anomaly_check.sufficient:
                abstentions.append({
                    "user_id": user_id, "metric": metric, "type": "anomaly",
                    "reason": anomaly_check.reason,
                })
            else:
                for a in detect_anomalies(user_id, metric, dates, values):
                    insights.append(_anomaly_to_insight(a))

    return {"insights": insights, "abstentions": abstentions}
