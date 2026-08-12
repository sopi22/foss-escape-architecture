"""Persistence and run-over-run comparison. JSON, not the brief's
provisional "experiment.yaml" -- see RESEARCH.txt for why: this is the
project's single persistent format (entropy budget: persistent formats =
1), and stdlib `json` avoids a dependency (PyYAML) that a plain
dict-of-dicts on disk doesn't actually need. The provisional name was
never a commitment to the format, only to persisting *something*.
"""

from __future__ import annotations

import json
from pathlib import Path

from .model import ComparedResult, Comparison, Observation, ProbeResult


def load_history(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def save_history(path: Path, history: dict) -> None:
    path.write_text(json.dumps(history, indent=2, sort_keys=True) + "\n")


def compare(history: dict, result: ProbeResult) -> Comparison:
    """DECISION (logged in RESEARCH.txt): NO_COMPARISON is used whenever
    either side of the comparison is UNKNOWN, not just when no prior
    record exists. An UNKNOWN carries no evidence either way, so treating
    it as UNCHANGED or CHANGED against a real PASS/FAIL would overstate
    what's actually known. NEW is reserved for a genuinely first-ever
    record of this assumption.
    """
    prior = history.get(result.assumption)

    if result.observation is Observation.UNKNOWN:
        return Comparison.NO_COMPARISON

    if prior is None:
        return Comparison.NEW

    prior_observation = Observation(prior["observation"])
    if prior_observation is Observation.UNKNOWN:
        return Comparison.NO_COMPARISON

    if prior_observation == result.observation:
        return Comparison.UNCHANGED
    return Comparison.CHANGED


def record(history: dict, result: ProbeResult) -> ComparedResult:
    """Compute this run's comparison against `history`, then update
    `history` in place with this run (mutates the dict; caller decides
    when to persist it via save_history)."""
    comparison = compare(history, result)
    history[result.assumption] = result.to_dict()
    return ComparedResult(result, comparison)
