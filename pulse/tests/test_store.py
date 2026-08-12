"""Comparison logic vs a prior run. Pure logic, synthetic data -- no
device needed.
"""

from pulse.model import Comparison, Observation, ProbeResult, now_iso
from pulse.store import compare, record


def _result(observation: Observation) -> ProbeResult:
    return ProbeResult("some_assumption", observation, "synthetic", now_iso())


def test_first_ever_run_is_new():
    history: dict = {}
    assert compare(history, _result(Observation.PASS)) is Comparison.NEW


def test_repeated_same_observation_is_unchanged():
    history: dict = {}
    record(history, _result(Observation.PASS))
    assert compare(history, _result(Observation.PASS)) is Comparison.UNCHANGED


def test_differing_observation_is_changed():
    history: dict = {}
    record(history, _result(Observation.PASS))
    assert compare(history, _result(Observation.FAIL)) is Comparison.CHANGED


def test_current_unknown_is_no_comparison_even_with_prior_pass():
    history: dict = {}
    record(history, _result(Observation.PASS))
    assert compare(history, _result(Observation.UNKNOWN)) is Comparison.NO_COMPARISON


def test_prior_unknown_is_no_comparison_even_with_current_pass():
    history: dict = {}
    record(history, _result(Observation.UNKNOWN))
    assert compare(history, _result(Observation.PASS)) is Comparison.NO_COMPARISON


def test_record_updates_history_in_place():
    history: dict = {}
    record(history, _result(Observation.PASS))
    assert history["some_assumption"]["observation"] == "PASS"
