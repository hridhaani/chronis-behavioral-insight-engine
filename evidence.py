"""Component 4: Evidence Sufficiency — gatekeeping before claims are made."""
from dataclasses import dataclass

MIN_TOTAL_DAYS_TREND = 14
MIN_HISTORY_ANOMALY = 10
MIN_CHANGE_PCT = 10.0


@dataclass
class EvidenceCheck:
    sufficient: bool
    reason: str = None


def check_trend_evidence(values: list) -> EvidenceCheck:
    if len(values) < MIN_TOTAL_DAYS_TREND:
        return EvidenceCheck(False, f"Only {len(values)} days available; need at least "
                                    f"{MIN_TOTAL_DAYS_TREND} for a reliable trend.")
    return EvidenceCheck(True)


def check_anomaly_evidence(values: list) -> EvidenceCheck:
    if len(values) < MIN_HISTORY_ANOMALY:
        return EvidenceCheck(False, f"Only {len(values)} days available; need at least "
                                    f"{MIN_HISTORY_ANOMALY} to establish a 'normal' range.")
    return EvidenceCheck(True)
