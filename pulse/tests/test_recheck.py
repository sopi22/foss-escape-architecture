"""Pure-logic tests for the periodic re-check runner -- no device, no
probes, no real RESEARCH.txt needed."""

from __future__ import annotations

from pulse.model import ComparedResult, Comparison, Observation, ProbeResult
from pulse.recheck import SECTION_MARKER, append_entry, format_entry


def _result(assumption: str, observation: Observation, comparison: Comparison) -> ComparedResult:
    return ComparedResult(
        ProbeResult(assumption, observation, "detail text", "2026-08-14T00:00:00+00:00"),
        comparison,
    )


def test_format_entry_uses_only_existing_model_fields():
    results = [
        _result("storage_write", Observation.PASS, Comparison.UNCHANGED),
        _result("settings_persist", Observation.FAIL, Comparison.CHANGED),
    ]
    entry = format_entry(results, "10.0.0.1:5555", "2026-08-14")

    assert "2026-08-14" in entry
    assert "10.0.0.1:5555" in entry
    assert "OBSERVATION=PASS" in entry
    assert "COMPARISON=UNCHANGED" in entry
    assert "OBSERVATION=FAIL" in entry
    assert "COMPARISON=CHANGED" in entry


def test_append_entry_requires_section_marker(tmp_path):
    research_txt = tmp_path / "RESEARCH.txt"
    research_txt.write_text("no marker here\n")

    try:
        append_entry(research_txt, "RE-CHECK (...)\n")
        assert False, "expected SystemExit when the section marker is missing"
    except SystemExit:
        pass


def test_append_entry_appends_after_existing_section(tmp_path):
    research_txt = tmp_path / "RESEARCH.txt"
    research_txt.write_text(f"{SECTION_MARKER}\nsome prose\n")

    append_entry(research_txt, "RE-CHECK (2026-08-14, device X):\n")

    text = research_txt.read_text()
    assert text.startswith(f"{SECTION_MARKER}\nsome prose\n")
    assert text.endswith("RE-CHECK (2026-08-14, device X):\n")
