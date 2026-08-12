"""CLI entrypoint. `--serial` is required, deliberately not
auto-detected from `adb devices` -- on a shared machine, silently picking
"whichever device happens to be connected" is exactly the kind of
implicit scope creep this project's device access rules rule out.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .adb import AdbShell
from .probes import ALL_PROBES
from .store import load_history, record, save_history

DEFAULT_HISTORY_PATH = Path("pulse_history.json")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run Pulse's confirmed probes against one adb-connected device."
    )
    parser.add_argument(
        "--serial",
        required=True,
        help="Device serial as shown by `adb devices` (e.g. 10.161.62.188:40139).",
    )
    parser.add_argument(
        "--history",
        type=Path,
        default=DEFAULT_HISTORY_PATH,
        help=f"Path to the JSON run-history file (default: {DEFAULT_HISTORY_PATH}).",
    )
    args = parser.parse_args(argv)

    shell = AdbShell(args.serial)
    history = load_history(args.history)

    compared_results = []
    for probe in ALL_PROBES:
        result = probe(shell)
        compared_results.append(record(history, result))

    save_history(args.history, history)

    for cr in compared_results:
        print(json.dumps(cr.to_dict()))

    return 0


if __name__ == "__main__":
    sys.exit(main())
