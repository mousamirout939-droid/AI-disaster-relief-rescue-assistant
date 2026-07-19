"""
Computes a 1-5 triage priority for a queue of disaster reports, so admins can
work the most urgent cases first. Combines AI severity, elapsed wait time,
and whether the report already has a dispatched team.
"""
import time
from typing import Dict, List

_SEVERITY_SCORE = {"low": 1, "moderate": 2, "high": 3, "critical": 4}


def compute_priority(report: Dict) -> int:
    severity_score = _SEVERITY_SCORE.get(report.get("ai_severity", "low"), 1)
    wait_minutes = (time.time() - report.get("created_at", time.time())) / 60
    wait_bonus = min(wait_minutes / 30, 2)  # up to +2 for reports waiting 60+ minutes
    already_dispatched = -2 if report.get("status") == "in_progress" else 0

    raw_score = severity_score + wait_bonus + already_dispatched
    return max(1, min(round(raw_score), 5))


def sort_by_priority(reports: List[Dict]) -> List[Dict]:
    return sorted(reports, key=compute_priority, reverse=True)
