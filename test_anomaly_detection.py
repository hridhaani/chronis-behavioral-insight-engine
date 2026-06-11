from src.anomaly_detection import detect_anomalies


def test_detects_obvious_outlier():
    values = [7, 7, 7, 7, 7, 7, 7, 7, 7, 20]  # last value is way off
    dates = [f"2026-01-{i+1:02d}" for i in range(10)]
    anomalies = detect_anomalies("U_test", "sleep_hours", dates, values)
    assert len(anomalies) == 1
    assert anomalies[0].date == "2026-01-10"


def test_no_anomalies_in_constant_series():
    values = [7] * 10
    dates = [f"2026-01-{i+1:02d}" for i in range(10)]
    assert detect_anomalies("U_test", "sleep_hours", dates, values) == []


def test_no_anomalies_with_insufficient_history():
    values = [7, 7, 7, 20]  # below MIN_HISTORY_FOR_ANOMALY
    dates = [f"2026-01-{i+1:02d}" for i in range(4)]
    assert detect_anomalies("U_test", "sleep_hours", dates, values) == []
