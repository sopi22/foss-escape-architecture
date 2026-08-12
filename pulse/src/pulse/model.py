"""The experimental model (brief, EXPERIMENTAL MODEL section): two
independent fields, never merged.
"""

from __future__ import annotations

import datetime
from dataclasses import dataclass
from enum import Enum


class Observation(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    UNKNOWN = "UNKNOWN"


class Comparison(str, Enum):
    NEW = "NEW"
    UNCHANGED = "UNCHANGED"
    CHANGED = "CHANGED"
    NO_COMPARISON = "NO_COMPARISON"


def now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


@dataclass(frozen=True)
class ProbeResult:
    """A single probe's outcome on a single run. `assumption` is the
    provisional, deliberately unambitious identifier for the assumption
    under test (e.g. "storage_write"), not a claim of architectural
    significance.
    """

    assumption: str
    observation: Observation
    detail: str
    timestamp: str

    def to_dict(self) -> dict:
        return {
            "assumption": self.assumption,
            "observation": self.observation.value,
            "detail": self.detail,
            "timestamp": self.timestamp,
        }

    @staticmethod
    def from_dict(data: dict) -> "ProbeResult":
        return ProbeResult(
            assumption=data["assumption"],
            observation=Observation(data["observation"]),
            detail=data["detail"],
            timestamp=data["timestamp"],
        )


@dataclass(frozen=True)
class ComparedResult:
    result: ProbeResult
    comparison: Comparison

    def to_dict(self) -> dict:
        d = self.result.to_dict()
        d["comparison"] = self.comparison.value
        return d
