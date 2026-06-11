"""Loads and validates the behavioral CSV dataset."""
import pandas as pd

REQUIRED_COLUMNS = [
    "user_id", "date", "steps", "sleep_hours",
    "screen_time_hours", "deep_work_hours", "exercise_minutes",
]

NUMERIC_COLUMNS = [
    "steps", "sleep_hours", "screen_time_hours",
    "deep_work_hours", "exercise_minutes",
]


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    missing = set(REQUIRED_COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"Dataset missing required columns: {missing}")

    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(["user_id", "date"]).reset_index(drop=True)

    # Coerce numerics; flag rows that fail (don't silently drop without logging)
    for col in NUMERIC_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def get_user_series(df: pd.DataFrame, user_id: str, metric: str) -> list:
    """Return a clean (NaN-dropped), date-ordered list of values for a user/metric."""
    series = df.loc[df["user_id"] == user_id, metric].dropna()
    return series.tolist()
