"""Manual periodic re-check runner.

Pulse's own research hypothesis includes being comparable *over time*
-- everything logged in R0-R4 was collected within one short session,
not across real elapsed time as the OS actually updates. This gives a
way to re-run the two confirmed probes later (e.g. after an Android
security patch or OS update lands on the test device) and log a real
COMPARISON state against the last run, in RESEARCH.md where a human
will actually read it alongside the rest of the reproducibility record.

This is NOT a new probe type (it runs the same two ALL_PROBES cli.py
runs) and NOT automation: it is meant to be invoked by hand,
occasionally. No cron, no background service -- the entropy budget's
"Background processes: 0" is unaffected.
"""

from __future__ import annotations

import argparse
import datetime
import sys
from pathlib import Path

from .adb import AdbShell
from .model import ComparedResult
from .probes import ALL_PROBES
from .store import load_history, record, save_history

DEFAULT_HISTORY_PATH = Path("pulse_history.json")
DEFAULT_RESEARCH_PATH = Path("../RESEARCH.md")
SECTION_MARKER = "10. PERIODIC RE-CHECK LOG"


def format_entry(
    compared_results: list[ComparedResult], serial: str, today: str
) -> str:
    """One dated block per re-check run. Fields are exactly the
    existing model's own (assumption, observation, comparison, detail)
    -- no new fields, no new report format."""
    lines = [f"\nRE-CHECK ({today}, device {serial}):"]
    for cr in compared_results:
        lines.append(
            f"  {cr.result.assumption}: OBSERVATION={cr.result.observation.value}, "
            f"COMPARISON={cr.comparison.value} -- {cr.result.detail}"
        )
    return "\n".join(lines) + "\n"


def append_entry(research_txt: Path, entry: str) -> None:
    if not research_txt.exists():
        raise SystemExit(f"{research_txt} not found")
    text = research_txt.read_text()
    if SECTION_MARKER not in text:
        raise SystemExit(
            f"{research_txt} has no {SECTION_MARKER!r} section -- "
            "add that section once before running this."
        )
    research_txt.write_text(text + entry)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Manually re-run Pulse's two confirmed probes against the "
            "currently connected device and log a dated "
            "OBSERVATION/COMPARISON entry to RESEARCH.md's periodic "
            "re-check log. Run this yourself, occasionally -- it is not "
            "scheduled and does not run in the background."
        )
    )
    parser.add_argument(
        "--serial",
        required=True,
        help="Device serial as shown by `adb devices`.",
    )
    parser.add_argument(
        "--history",
        type=Path,
        default=DEFAULT_HISTORY_PATH,
        help=f"Path to the JSON run-history file (default: {DEFAULT_HISTORY_PATH}).",
    )
    parser.add_argument(
        "--research-txt",
        type=Path,
        default=DEFAULT_RESEARCH_PATH,
        help=f"Path to RESEARCH.md to append the dated entry to (default: {DEFAULT_RESEARCH_PATH}).",
    )
    args = parser.parse_args(argv)

    shell = AdbShell(args.serial)
    history = load_history(args.history)

    compared_results = [record(history, probe(shell)) for probe in ALL_PROBES]
    save_history(args.history, history)

    today = datetime.date.today().isoformat()
    entry = format_entry(compared_results, args.serial, today)
    append_entry(args.research_txt, entry)

    for cr in compared_results:
        print(f"{cr.result.assumption}: {cr.result.observation.value} ({cr.comparison.value})")
    print(f"Appended to {args.research_txt}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
