from src.pattern_detection import detect_pattern


def test_detects_clear_increase():
    # baseline ~5000 for 23 days, recent ~7000 for 7 days -> +40%
    values = [5000] * 23 + [7000] * 7
    p = detect_pattern("U_test", "steps", values)
    assert p is not None
    assert p.direction == "increase"
    assert p.pct_change > 10


def test_no_pattern_when_change_too_small():
    values = [5000] * 23 + [5100] * 7  # ~2% change
    p = detect_pattern("U_test", "steps", values)
    assert p is None


def test_returns_none_with_insufficient_history():
    values = [5000] * 10  # below MIN_TOTAL_DAYS
    p = detect_pattern("U_test", "steps", values)
    assert p is None
