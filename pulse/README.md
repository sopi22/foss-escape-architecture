# pulse -- Experiment 001 probe harness

What this is: a minimal runner for the two confirmed probes
(probe_storage_write, probe_settings_persist) against one adb-connected
Android device, with run-over-run comparison (NEW/UNCHANGED/CHANGED/
NO_COMPARISON) persisted to a local JSON history file.

See ../README.md and ../RESEARCH.md for the research question,
hypothesis, and per-probe justification. This file only covers running
the code.

## DEPENDENCIES
Runtime: none beyond the Python standard library.
Dev/test: pytest (see pyproject.toml).
Transport: the system `adb` binary must be on PATH, and a device must
already be connected (`adb devices` shows it) -- this package does not
manage pairing/connecting itself.

## SETUP
    cd pulse
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -e ".[dev]"

## RUN THE PROBES
    pulse-run --serial <serial-as-shown-by-adb-devices>

    # example:
    pulse-run --serial 10.161.62.188:40139

Each run prints one JSON line per probe result and appends to
pulse_history.json (in the current directory by default; override with
--history <path>) so the next run can report NEW/UNCHANGED/CHANGED for
the same assumption.

## RE-CHECK LATER
Pulse's own hypothesis includes being comparable over time, but every
run logged so far happened within one short session. `pulse-recheck`
is a manual-trigger way to re-run the same two probes later (e.g.
after an Android security patch or OS update lands on the test
device) and log the result -- not a new probe, not scheduled, not a
background process:

    pulse-recheck --serial <serial-as-shown-by-adb-devices>

    # example:
    pulse-recheck --serial 10.161.62.188:40139

This does everything `pulse-run` does (same two probes, same
pulse_history.json, same NEW/UNCHANGED/CHANGED/NO_COMPARISON logic)
and additionally appends one dated OBSERVATION/COMPARISON block to
../RESEARCH.md's "PERIODIC RE-CHECK LOG" section (override the
target file with --research-txt if not running from this directory).
Run this yourself, occasionally -- there is nothing to set up or leave
running.

## RUN THE TESTS
    pytest

Tests in test_store.py are pure logic and need no device. Tests in
test_probes_live.py run the actual probes against a connected device
(including one deliberately-triggered FAIL case) and are skipped
automatically if `adb devices` shows nothing connected.
