import pandas as pd
from src.insight_generator import generate_insights


def make_df():
    rows = []
    # 30 days, steps trending down from ~8000 to ~6000
    for i in range(30):
        steps = 8000 - (i * 60) if i >= 23 else 8000
        rows.append({
            "user_id": "U_test", "date": f"2026-01-{i+1:02d}",
            "steps": steps, "sleep_hours": 7.0, "screen_time_hours": 5.0,
            "deep_work_hours": 3.0, "exercise_minutes": 30,
        })
    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"])
    return df


def test_generates_pattern_insight_with_confidence():
    df = make_df()
    result = generate_insights(df)
    pattern_insights = [i for i in result["insights"] if i["type"] == "pattern"]
    assert any(i["metric"] == "steps" for i in pattern_insights)
    for i in pattern_insights:
        assert 0 <= i["confidence"] <= 0.95


def test_abstains_on_constant_metrics():
    df = make_df()
    result = generate_insights(df)
    # sleep_hours is constant -> no pattern, possibly an abstention or no-op
    sleep_abstentions = [a for a in result["abstentions"]
                         if a["metric"] == "sleep_hours" and a["user_id"] == "U_test"]
    assert len(sleep_abstentions) >= 1
